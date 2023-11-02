import logging
import numpy as np
from .utils_box import boxes2bbox


class TextLineCfg:
    MAX_HORIZONTAL_GAP_REL = 3
    HORIZONTAL_OVERLAP_MARGIN_REL = 1
    MIN_V_OVERLAPS = 0.4
    MIN_SIZE_SIM = 0.4


class TextLineBuilder:
    config = TextLineCfg()
    box_table = None
    graph = None  # succession links between boxes

    def get_successions(self, index):
        box = self.text_proposals[index]
        results = []
        h = box[3] - box[1] + 1
        lbound = int(
            max(box[0] + 1, box[2] - self.config.HORIZONTAL_OVERLAP_MARGIN_REL * h)
        )
        rbound = int(box[2] + self.config.MAX_HORIZONTAL_GAP_REL * h)
        for left in range(max(lbound, 0), min(rbound, self.im_size[1])):
            adj_box_indices = self.boxes_table[left]
            for adj_box_index in adj_box_indices:
                if self.meet_v_iou(adj_box_index, index):
                    results.append(adj_box_index)
            if len(results) != 0:
                return results
        return results

    def meet_v_iou(self, index1, index2):
        def overlaps_v(index1, index2):
            h1 = self.heights[index1]
            h2 = self.heights[index2]
            y0 = max(self.text_proposals[index2][1], self.text_proposals[index1][1])
            y1 = min(self.text_proposals[index2][3], self.text_proposals[index1][3])
            return max(0, y1 - y0 + 1) / min(h1, h2)

        def size_similarity(index1, index2):
            h1 = self.heights[index1]
            h2 = self.heights[index2]
            return min(h1, h2) / max(h1, h2)

        return all(
            [
                overlaps_v(index1, index2) >= self.config.MIN_V_OVERLAPS,
                size_similarity(index1, index2) >= self.config.MIN_SIZE_SIM,
            ]
        )

    def build_graph(self, text_proposals, im_size=None):
        text_proposals = np.array(text_proposals)
        im_size = im_size or (
            text_proposals[:, 1::2].max().astype(int) + 1,
            text_proposals[:, ::2].max().astype(int) + 1,
        )
        self.text_proposals = text_proposals
        self.im_size = im_size
        self.heights = text_proposals[:, 3] - text_proposals[:, 1] + 1

        boxes_table = [[] for _ in range(self.im_size[1])]
        for index, box in enumerate(text_proposals):
            boxes_table[int(box[0])].append(index)
        self.boxes_table = boxes_table

        graph = np.zeros((text_proposals.shape[0], text_proposals.shape[0]), np.bool)

        for index, box in enumerate(text_proposals):
            successions = self.get_successions(index)
            if len(successions) == 0:
                continue
            succession_index = successions[0]
            graph[index, succession_index] = True

        self.graph = graph

    def get_line_boxes_index(self):
        sub_graphs = []
        for index in range(self.graph.shape[0]):
            if not self.graph[:, index].any() and self.graph[index, :].any():
                v = index
                sub_graphs.append([v])
                while self.graph[v, :].any():
                    v = np.where(self.graph[v, :])[0][0]
                    if v in sub_graphs[-1]:
                        break
                    sub_graphs[-1].append(v)
        sub_graphs_nodes = []
        for graph in sub_graphs:
            sub_graphs_nodes.extend(graph)
        standalones = list(
            [v] for v in range(self.graph.shape[0]) if v not in sub_graphs_nodes
        )
        sub_graphs.extend(standalones)
        return sub_graphs

    def get_line_boxes(self):
        line_boxes = list(self.text_proposals[sg] for sg in self.get_line_boxes_index())
        return line_boxes

    def get_line_bbox(self):
        line_boxes = self.get_line_boxes()
        return list(boxes2bbox(box) for box in line_boxes)

    def get_line_info(self):
        """
        return: line_boxes_index, line_boxes, line_bbox
        line_boxes_index: [idxs, idxs]
        line_boxes:[boxes, boxes]
        line_boxes_bbox: [box, box]
        """
        line_boxes_index = self.get_line_boxes_index()
        line_boxes = list(self.text_proposals[sg] for sg in line_boxes_index)
        line_boxes_bbox = list(boxes2bbox(box) for box in line_boxes)
        return line_boxes_index, line_boxes, line_boxes_bbox
