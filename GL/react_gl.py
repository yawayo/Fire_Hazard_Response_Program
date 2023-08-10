from OpenGL.GL import *
import heapq
import pywavefront
import math

class route_search:

    def __init__(self):
        super().__init__()

    def search_path(self, graph, first):
        distance = {node: [float('inf'), first] for node in graph}
        distance[first] = [0, first]
        queue = []

        heapq.heappush(queue, [distance[first][0], first])

        while queue:
            current_distance, current_node = heapq.heappop(queue)

            if distance[current_node][0] < current_distance:
                continue

            for next_node, weight in graph[current_node].items():
                total_distance = current_distance + weight

                if total_distance < distance[next_node][0]:
                    # 다음 노드까지 총 거리와 어떤 노드를 통해서 왔는지 입력
                    distance[next_node] = [total_distance, current_node]
                    heapq.heappush(queue, [total_distance, next_node])
        # 마지막 노드부터 첫번째 노드까지 순서대로 출력
        path_list = []

        min_distance = []
        min_distance.append(distance['escape00'])
        min_distance.append(distance['escape01'])

        min_escape_num = min_distance.index(min(min_distance))
        last = 'escape' + str(min_escape_num).zfill(2)

        path = last

        path_list.append(last)
        while distance[path][1] != first:
            path_list.append(distance[path][1])
            path = distance[path][1]
        path_list.append(first)
        path_list.reverse()

        return path_list

    def search(self, node, start_node):
        return self.search_path(node, start_node)

class eva_draw:
    def __init__(self):
        super().__init__()

        self.Fire = [False for _ in range(5)]

        self.height = 0.4

        self.Watch_floor = 0

        self.Start_floor = 1
        self.Start_room = 0
        self.node_point = None
        self.room_position = [[-2.515, -0.815],
                              [-1.8, -0.74],
                              [-0.355, -0.115],
                              [0.355, 0.215],
                              [1.065, 0.54],
                              [1.775, 0.87],
                              [2.485, 1.395]]

        self.var_init()
        self.load_obj()

        self.path_route = None

    def var_init(self):
        self.color()
        self.rs = route_search()

        self.node_point = {
            # 1 Floor room ###########################################################################

            # Escape Node
            'room00': [-0.61, -0.3125],
            'room01': [0.21, 0.20],
            'room02': [-0.1665, -0.3325],

            # hallway
            'hallway00': [-0.263, 0.546],
            'hallway01': [-0.263, 0.10675],

            'stair0': [0.00, 0.73],
            'escape00': [0.0665, -0.7325],

            # 2 Floor room ###########################################################################

            # room
            'room10': [-2.515, -0.815],
            'room11': [-1.8, -0.74],
            'room12': [-0.355, -0.115],
            'room13': [0.355, 0.215],
            'room14': [1.065, 0.54],
            'room15': [1.775, 0.87],
            'room16': [2.485, 1.395],

            # hallway
            'hallway20': [-2.16, -0.245],
            'hallway21': [-1.8, -0.245],
            'hallway22': [-1.436, -0.245],
            'hallway23': [-1.075, -0.245],
            'hallway24': [-0.79, -0.245],
            'hallway25': [-0.79, 0.028],
            'hallway26': [-0.79, 0.30],
            'hallway27': [-0.527, 0.423],
            'hallway28': [-0.263, 0.546],
            'hallway29': [0, 0.668],
            'hallway30': [0.355, 0.825],
            'hallway31': [0.71, 0.998],
            'hallway32': [1.065, 1.17],
            'hallway33': [1.421, 1.333],
            'hallway34': [1.775, 1.495],
            'hallway35': [2.13, 1.655],

            # Stair
            'stair1': [-0.10, 0.73],

            # 3 Floor room ###########################################################################

            # room
            'room20': [-2.515, -0.815],
            'room21': [-1.8, -0.74],
            'room22': [-0.355, -0.115],
            'room23': [0.355, 0.215],
            'room24': [1.065, 0.54],
            'room25': [1.775, 0.87],
            'room26': [2.485, 1.395],

            # hallway
            'hallway40': [-2.16, -0.245],
            'hallway41': [-1.8, -0.245],
            'hallway42': [-1.436, -0.245],
            'hallway43': [-1.075, -0.245],
            'hallway44': [-0.79, -0.245],
            'hallway45': [-0.79, 0.028],
            'hallway46': [-0.79, 0.30],
            'hallway47': [-0.527, 0.423],
            'hallway48': [-0.263, 0.546],
            'hallway49': [0, 0.668],
            'hallway50': [0.355, 0.825],
            'hallway51': [0.71, 0.998],
            'hallway52': [1.065, 1.17],
            'hallway53': [1.421, 1.333],
            'hallway54': [1.775, 1.495],
            'hallway55': [2.13, 1.655],

            # Stair
            'stair2': [-0.10, 0.73],

            # 4 Floor room ###########################################################################

            # room
            'room30': [-2.515, -0.815],
            'room31': [-1.8, -0.74],
            'room32': [-0.355, -0.115],
            'room33': [0.355, 0.215],
            'room34': [1.065, 0.54],
            'room35': [1.775, 0.87],
            'room36': [2.485, 1.395],

            # hallway
            'hallway60': [-2.16, -0.245],
            'hallway61': [-1.8, -0.245],
            'hallway62': [-1.436, -0.245],
            'hallway63': [-1.075, -0.245],
            'hallway64': [-0.79, -0.245],
            'hallway65': [-0.79, 0.028],
            'hallway66': [-0.79, 0.30],
            'hallway67': [-0.527, 0.423],
            'hallway68': [-0.263, 0.546],
            'hallway69': [0, 0.668],
            'hallway70': [0.355, 0.825],
            'hallway71': [0.71, 0.998],
            'hallway72': [1.065, 1.17],
            'hallway73': [1.421, 1.333],
            'hallway74': [1.775, 1.495],
            'hallway75': [2.13, 1.655],

            # Stair
            'stair3': [-0.10, 0.73],

            # 5 Floor room ###########################################################################

            # room
            'room40': [-2.515, -0.815],
            'room41': [-1.8, -0.74],
            'room42': [-0.355, -0.115],
            'room43': [0.355, 0.215],
            'room44': [1.065, 0.54],
            'room45': [1.775, 0.87],
            'room46': [2.485, 1.395],

            # hallway
            'hallway80': [-2.16, -0.245],
            'hallway81': [-1.8, -0.245],
            'hallway82': [-1.436, -0.245],
            'hallway83': [-1.075, -0.245],
            'hallway84': [-0.79, -0.245],
            'hallway85': [-0.79, 0.028],
            'hallway86': [-0.79, 0.30],
            'hallway87': [-0.527, 0.423],
            'hallway88': [-0.263, 0.546],
            'hallway89': [0, 0.668],
            'hallway90': [0.355, 0.825],
            'hallway91': [0.71, 0.998],
            'hallway92': [1.065, 1.17],
            'hallway93': [1.421, 1.333],
            'hallway94': [1.775, 1.495],
            'hallway95': [2.13, 1.655],

            # Stair
            'stair4': [-0.10, 0.73],

            # Stair
            'stair5': [-0.10, 0.73],

            # Stair middle
            'Dstair01': [-0.084, 0.90],
            'Cstair01': [0, 1.18],
            'Ustair01': [0.084, 0.90],
            'Dstair12': [-0.084, 0.90],
            'Cstair12': [0, 1.18],
            'Ustair12': [0.084, 0.90],
            'Dstair23': [-0.084, 0.90],
            'Cstair23': [0, 1.18],
            'Ustair23': [0.084, 0.90],
            'Dstair34': [-0.084, 0.90],
            'Cstair34': [0, 1.18],
            'Ustair34': [0.084, 0.90],
            'Dstair45': [-0.084, 0.90],
            'Cstair45': [0, 1.18],
            'Ustair45': [0.084, 0.90],

            # Roof
            'escape01': [-0.527, 0.423],
        }

    def draw_Danger_Building(self):
        Fire = False
        for status in self.Fire:
            if status:
                Fire = True
        if Fire:
            if self.Watch_floor == 0:
                self.draw_Obj(self.room_position[2][0], self.room_position[2][1], self.height * self.Start_floor)
            else:
                self.draw_Obj(self.room_position[self.Start_room][0], self.room_position[self.Start_room][1], self.height * self.Start_floor)

            Thickness = 0.1
            size = 0.2
            if self.path_route is not None:
                for idx in range(len(self.path_route) - 1):
                    if 'room' in self.path_route[idx]:
                        height_point = self.height * int(self.path_route[idx][-2])
                        self.draw_Arrow(self.node_point[self.path_route[idx]][0], self.node_point[self.path_route[idx]][1], height_point,
                                        self.node_point[self.path_route[idx + 1]][0], self.node_point[self.path_route[idx + 1]][1], height_point,
                                        Thickness, size)

                    elif 'hallway' in self.path_route[idx]:
                        height_point = self.height * int(int(self.path_route[idx][-2:]) / 20.0)
                        self.draw_Arrow(self.node_point[self.path_route[idx]][0], self.node_point[self.path_route[idx]][1], height_point,
                                        self.node_point[self.path_route[idx + 1]][0], self.node_point[self.path_route[idx + 1]][1], height_point,
                                        Thickness, size)

                    elif 'stair' in self.path_route[idx]:
                        if 'stair' in self.path_route[idx + 1]:
                            floor_class = str(min(int(self.path_route[idx][-1]), int(self.path_route[idx + 1][-1]))) + str(max(int(self.path_route[idx][-1]), int(self.path_route[idx + 1][-1])))
                            start_node = 'Ustair' + floor_class
                            center_node = 'Cstair' + floor_class
                            end_node = 'Dstair' + floor_class
                            start_height_point = self.height * max(int(self.path_route[idx][-1]), int(self.path_route[idx + 1][-1]))
                            center_height_point = self.height * ((int(self.path_route[idx][-1]) + int(self.path_route[idx + 1][-1])) / 2)
                            end_height_point = self.height * min(int(self.path_route[idx][-1]), int(self.path_route[idx + 1][-1]))
                            if int(self.path_route[idx + 1][-1]) != 0:
                                if int(self.path_route[idx][-1]) > int(self.path_route[idx + 1][-1]):
                                    self.draw_Arrow(self.node_point[start_node][0], self.node_point[start_node][1], start_height_point,
                                                    self.node_point[start_node][0], self.node_point[center_node][1], center_height_point,
                                                    Thickness, size)
                                    self.draw_Arrow(self.node_point[center_node][0] + 1, self.node_point[center_node][1] + 0.1, center_height_point,
                                                    self.node_point[center_node][0] - 1, self.node_point[center_node][1] + 0.1, center_height_point,
                                                    Thickness, size)
                                    self.draw_Arrow(self.node_point[end_node][0], self.node_point[center_node][1], center_height_point,
                                                    self.node_point[end_node][0], self.node_point[end_node][1], end_height_point,
                                                    Thickness, size)
                                    self.draw_Arrow(self.node_point[center_node][0] - 1, self.node_point[end_node][1] - 0.1, end_height_point,
                                                    self.node_point[center_node][0] + 1, self.node_point[end_node][1] - 0.1, end_height_point,
                                                    Thickness, size)

                                else:
                                    self.draw_Arrow(self.node_point[end_node][0], self.node_point[end_node][1], end_height_point,
                                                    self.node_point[end_node][0], self.node_point[center_node][1], center_height_point,
                                                    Thickness, size)
                                    self.draw_Arrow(self.node_point[center_node][0] - 1, self.node_point[center_node][1] + 0.1, center_height_point,
                                                    self.node_point[center_node][0] + 1, self.node_point[center_node][1] + 0.1, center_height_point,
                                                    Thickness, size)
                                    self.draw_Arrow(self.node_point[start_node][0], self.node_point[center_node][1], center_height_point,
                                                    self.node_point[start_node][0], self.node_point[start_node][1], start_height_point,
                                                    Thickness, size)
                                    self.draw_Arrow(self.node_point[center_node][0] + 1, self.node_point[start_node][1] - 0.1, start_height_point,
                                                    self.node_point[center_node][0] - 1, self.node_point[start_node][1] - 0.1, start_height_point,
                                                    Thickness, size)
                            else:
                                if int(self.path_route[idx][-1]) > int(self.path_route[idx + 1][-1]):
                                    self.draw_Arrow(self.node_point[start_node][0], self.node_point[start_node][1], start_height_point,
                                                    self.node_point[start_node][0], self.node_point[center_node][1], center_height_point,
                                                    Thickness, size)
                                    self.draw_Arrow(self.node_point[center_node][0] + 1, self.node_point[center_node][1] + 0.1, center_height_point,
                                                    self.node_point[center_node][0] - 1, self.node_point[center_node][1] + 0.1, center_height_point,
                                                    Thickness, size)
                                    self.draw_Arrow(self.node_point[end_node][0], self.node_point[center_node][1], center_height_point,
                                                    self.node_point[end_node][0], self.node_point[end_node][1], end_height_point,
                                                    Thickness, size)

                                else:
                                    self.draw_Arrow(self.node_point[end_node][0], self.node_point[end_node][1], end_height_point,
                                                    self.node_point[end_node][0], self.node_point[center_node][1], center_height_point,
                                                    Thickness, size)
                                    self.draw_Arrow(self.node_point[center_node][0] + 1, self.node_point[center_node][1] + 0.1, center_height_point,
                                                    self.node_point[center_node][0] - 1, self.node_point[center_node][1] + 0.1, center_height_point,
                                                    Thickness, size)
                                    self.draw_Arrow(self.node_point[start_node][0], self.node_point[center_node][1], center_height_point,
                                                    self.node_point[start_node][0], self.node_point[start_node][1], start_height_point,
                                                    Thickness, size)

                        else:
                            height_point = self.height * int(self.path_route[idx][-1:])
                            self.draw_Arrow(self.node_point[self.path_route[idx]][0], self.node_point[self.path_route[idx]][1], height_point,
                                            self.node_point[self.path_route[idx + 1]][0], self.node_point[self.path_route[idx + 1]][1], height_point,
                                            Thickness, size)

    def draw_Danger_Floor_3D(self):
        # wy_node = ['room00', 'room01', 'room02', 'hallway00', 'hallway01', 'escape00', 'stair0']
        # glColor(self.allow_color[0], self.allow_color[1], self.allow_color[2], self.allow_color[3])
        # glPointSize(5.0)
        # glBegin(GL_POINTS)
        # for node in wy_node:
        #     glVertex3fv(self.node_point[node] + [0.01])
        # glEnd()
        #

        Fire = False
        for status in self.Fire:
            if status:
                Fire = True
        if Fire:
            if self.Watch_floor == self.Start_floor:
                if self.Watch_floor == 0:
                    self.draw_Obj(self.room_position[2][0], self.room_position[2][1], self.height * self.Watch_floor)
                else:
                    self.draw_Obj(self.room_position[self.Start_room][0], self.room_position[self.Start_room][1], self.height * self.Watch_floor)

            Thickness = 0.1
            size = 0.2
            if self.path_route is not None:
                for idx in range(len(self.path_route) - 1):
                    if 'room' in self.path_route[idx]:
                        if int(self.path_route[idx][-2]) == self.Watch_floor:
                            height_point = self.height * int(self.path_route[idx][-2])
                            self.draw_Arrow(self.node_point[self.path_route[idx]][0], self.node_point[self.path_route[idx]][1], height_point,
                                            self.node_point[self.path_route[idx + 1]][0], self.node_point[self.path_route[idx + 1]][1], height_point,
                                            Thickness, size)

                    elif 'hallway' in self.path_route[idx]:
                        if (int(int(self.path_route[idx][-2:]) / 20)) == self.Watch_floor:
                            height_point = self.height * (int(int(self.path_route[idx][-2:]) / 20))
                            self.draw_Arrow(self.node_point[self.path_route[idx]][0], self.node_point[self.path_route[idx]][1], height_point,
                                            self.node_point[self.path_route[idx + 1]][0], self.node_point[self.path_route[idx + 1]][1], height_point,
                                            Thickness, size)

                    elif 'stair' in self.path_route[idx]:
                        if 'stair' in self.path_route[idx + 1]:
                            if (int(self.path_route[idx][-1]) == self.Watch_floor) or (int(self.path_route[idx + 1][-1]) == self.Watch_floor):
                                floor_class = str(min(int(self.path_route[idx][-1]), int(self.path_route[idx + 1][-1]))) + str(max(int(self.path_route[idx][-1]), int(self.path_route[idx + 1][-1])))
                                start_node = 'Ustair' + floor_class
                                center_node = 'Cstair' + floor_class
                                end_node = 'Dstair' + floor_class
                                start_height_point = self.height * max(int(self.path_route[idx][-1]), int(self.path_route[idx + 1][-1]))
                                center_height_point = self.height * ((int(self.path_route[idx][-1]) + int(self.path_route[idx + 1][-1])) / 2)
                                end_height_point = self.height * min(int(self.path_route[idx][-1]), int(self.path_route[idx + 1][-1]))
                                if int(self.path_route[idx][-1]) > int(self.path_route[idx + 1][-1]):
                                    self.draw_Arrow(self.node_point[start_node][0], self.node_point[start_node][1], start_height_point,
                                                    self.node_point[start_node][0], self.node_point[center_node][1], center_height_point,
                                                    Thickness, size)
                                    self.draw_Arrow(self.node_point[center_node][0] + 1, self.node_point[center_node][1] + 0.1, center_height_point,
                                                    self.node_point[center_node][0] - 1, self.node_point[center_node][1] + 0.1, center_height_point,
                                                    Thickness, size)
                                    self.draw_Arrow(self.node_point[end_node][0], self.node_point[center_node][1], center_height_point,
                                                    self.node_point[end_node][0], self.node_point[end_node][1], end_height_point,
                                                    Thickness, size)
                                    if (int(self.path_route[idx][-1]) == self.Watch_floor) and ('stair' in self.path_route[idx - 1]):
                                        self.draw_Arrow(self.node_point[center_node][0] - 1, self.node_point[end_node][1] - 0.07, start_height_point,
                                                        self.node_point[center_node][0] + 1, self.node_point[end_node][1] - 0.07, start_height_point,
                                                        Thickness, size)
                                else:
                                    self.draw_Arrow(self.node_point[end_node][0], self.node_point[end_node][1], end_height_point,
                                                    self.node_point[end_node][0], self.node_point[center_node][1], center_height_point,
                                                    Thickness, size)
                                    self.draw_Arrow(self.node_point[center_node][0] - 1, self.node_point[center_node][1] + 0.1, center_height_point,
                                                    self.node_point[center_node][0] + 1, self.node_point[center_node][1] + 0.1, center_height_point,
                                                    Thickness, size)
                                    self.draw_Arrow(self.node_point[start_node][0], self.node_point[center_node][1], center_height_point,
                                                    self.node_point[start_node][0], self.node_point[start_node][1], start_height_point,
                                                    Thickness, size)
                                    if (int(self.path_route[idx][-1]) == self.Watch_floor) and ('stair' in self.path_route[idx - 1]):
                                        self.draw_Arrow(self.node_point[center_node][0] + 1, self.node_point[end_node][1] - 0.07, end_height_point,
                                                        self.node_point[center_node][0] - 1, self.node_point[end_node][1] - 0.07, end_height_point,
                                                        Thickness, size)
                        else:
                            height_point = self.height * int(self.path_route[idx][-1:])
                            self.draw_Arrow(self.node_point[self.path_route[idx]][0], self.node_point[self.path_route[idx]][1], height_point,
                                            self.node_point[self.path_route[idx + 1]][0], self.node_point[self.path_route[idx + 1]][1], height_point,
                                            Thickness, size)


    def draw_Danger_Floor_2D(self):
        Fire = False
        for status in self.Fire:
            if status:
                Fire = True
        if Fire:
            if self.Watch_floor == self.Start_floor:
                if self.Watch_floor == 0:
                    self.draw_Obj(self.room_position[2][0], self.room_position[2][1], self.height * self.Watch_floor)
                else:
                    self.draw_Obj(self.room_position[self.Start_room][0], self.room_position[self.Start_room][1], self.height * self.Watch_floor)

            Thickness = 0.1
            size = 0.2
            if self.path_route is not None:
                for idx in range(len(self.path_route) - 1):
                    if 'room' in self.path_route[idx]:
                        if int(self.path_route[idx][-2]) == self.Watch_floor:
                            self.draw_Arrow(self.node_point[self.path_route[idx]][0], self.node_point[self.path_route[idx]][1], 0.0,
                                            self.node_point[self.path_route[idx + 1]][0], self.node_point[self.path_route[idx + 1]][1], 0.0,
                                            Thickness, size)

                    elif 'hallway' in self.path_route[idx]:
                        if (int(int(self.path_route[idx][-2:]) / 20)) == self.Watch_floor:
                            self.draw_Arrow(self.node_point[self.path_route[idx]][0], self.node_point[self.path_route[idx]][1], 0.0,
                                            self.node_point[self.path_route[idx + 1]][0], self.node_point[self.path_route[idx + 1]][1], 0.0,
                                            Thickness, size)

                    elif 'stair' in self.path_route[idx]:
                        if 'stair' in self.path_route[idx + 1]:
                            if int(self.path_route[idx][-1]) == self.Watch_floor:
                                floor_class = str(min(int(self.path_route[idx][-1]), int(self.path_route[idx + 1][-1]))) + str(max(int(self.path_route[idx][-1]), int(self.path_route[idx + 1][-1])))
                                start_node = 'Ustair' + floor_class
                                center_node = 'Cstair' + floor_class
                                end_node = 'Dstair' + floor_class
                                if int(self.path_route[idx][-1]) > int(self.path_route[idx + 1][-1]):
                                    self.draw_Arrow(self.node_point[start_node][0], self.node_point[start_node][1], 0.0,
                                                    self.node_point[start_node][0], self.node_point[center_node][1], 0.0,
                                                    Thickness, size)
                                    self.draw_Arrow(self.node_point[center_node][0] + 1, self.node_point[center_node][1], 0.0,
                                                    self.node_point[center_node][0] - 1, self.node_point[center_node][1], 0.0,
                                                    Thickness, size)
                                    self.draw_Arrow(self.node_point[end_node][0], self.node_point[center_node][1], 0.0,
                                                    self.node_point[end_node][0], self.node_point[end_node][1], 0.0,
                                                    Thickness, size)
                                else:
                                    self.draw_Arrow(self.node_point[end_node][0], self.node_point[end_node][1], 0.0,
                                                    self.node_point[end_node][0], self.node_point[center_node][1], 0.0,
                                                    Thickness, size)
                                    self.draw_Arrow(self.node_point[center_node][0] - 1, self.node_point[center_node][1], 0.0,
                                                    self.node_point[center_node][0] + 1, self.node_point[center_node][1], 0.0,
                                                    Thickness, size)
                                    self.draw_Arrow(self.node_point[start_node][0], self.node_point[center_node][1], 0.0,
                                                    self.node_point[start_node][0], self.node_point[start_node][1], 0.0,
                                                    Thickness, size)

    def color(self):
            self.human_color = [0.5, 0.0, 0.0, 1.0]
            self.allow_color = [1.0, 0.0, 0.0, 1.0]

    def load_obj(self):
        global scene, scene_scale
        scene = pywavefront.Wavefront('obj/Realistic_White_Male_Low_Poly.obj',
                                      collect_faces=True)
        scene.parse()

        scene_box = (scene.vertices[0], scene.vertices[0])

        for vertex in scene.vertices:
            min_v = [min(scene_box[0][i], vertex[i]) for i in range(3)]
            max_v = [max(scene_box[1][i], vertex[i]) for i in range(3)]
            scene_box = (min_v, max_v)

        scaled_size = 0.0001
        scene_size = [scaled_size * (scene_box[1][i] + scene_box[0][i]) / 2 for i in range(3)]
        max_scene_size = max(scene_size)
        scene_scale = [max_scene_size for i in range(3)]

    def draw_Obj(self, x, y, z):
        glPushMatrix()
        glTranslatef(x, y, z)
        glRotatef(90.0, 1.0, 0.0, 0.0)
        glScalef(*scene_scale)

        # for mesh in scene.mesh_list:
        #     glBegin(GL_TRIANGLES)
        #     glColor(self.human_color[0], self.human_color[1], self.human_color[2], self.human_color[3])
        #     for face in mesh.faces:
        #         for vertex_i in face:
        #             glVertex3f(*scene.vertices[vertex_i])
        #     glEnd()
        glPopMatrix()

    def draw_Arrow(self, x1, y1, z1, x2, y2, z2, Thickness, size):
        fly_value = 0.1
        glPushMatrix()
        glTranslatef((x1 + x2) / 2, (y1 + y2) / 2, (z1 + z2) / 2)
        glScalef(size, size, size)

        point_dif = [x2 - x1, y2 - y1, z2 - z1]
        point_rad_XY = (math.atan2(point_dif[1], point_dif[0]) * 180) / math.pi
        point_rad_YZ = (math.atan2(point_dif[2], point_dif[1]) * 180) / math.pi

        glRotatef(point_rad_XY, 0.0, 0.0, 1.0)
        if point_dif[2] != 0:
            if point_rad_XY > 0:
                glRotatef(point_rad_YZ * -1, 0.0, 1.0, 0.0)
            else:
                glRotatef(point_rad_YZ + 180, 0.0, 1.0, 0.0)

        all_points = [[-0.5, 0.1],
                      [-0.5, -0.1],
                      [0.2, -0.1],
                      [0.2, -0.3],
                      [0.5, -0.0],
                      [0.2, 0.3],
                      [0.2, 0.1],
                      [-0.5, 0.1]]
        points4 = all_points.copy()
        del points4[3:6]
        points3 = all_points[3:6]

        glColor(self.allow_color[0], self.allow_color[1], self.allow_color[2], self.allow_color[3])
        glBegin(GL_QUAD_STRIP)
        for point in all_points:
            glVertex3fv(point + [fly_value])
            glVertex3fv(point + [fly_value + Thickness])
        glEnd()
        glBegin(GL_POLYGON)
        for point in points3:
            glVertex3fv(point + [fly_value + Thickness])
        glEnd()
        glBegin(GL_POLYGON)
        for point in points4:
            glVertex3fv(point + [fly_value + Thickness])
        glEnd()
        glBegin(GL_POLYGON)
        for point in points3:
            glVertex3fv(point + [fly_value])
        glEnd()
        glBegin(GL_POLYGON)
        for point in points4:
            glVertex3fv(point + [fly_value])
        glEnd()

        glColor(0, 0, 0, 1)
        glLineWidth(3.0)
        glBegin(GL_LINE_LOOP)
        for point in all_points:
            glVertex3fv(point + [fly_value + Thickness])
        glEnd()
        glBegin(GL_LINE_LOOP)
        for point in all_points:
            glVertex3fv(point + [fly_value])
        glEnd()
        glBegin(GL_LINES)
        for point in all_points:
            glVertex3fv(point + [fly_value + Thickness])
            glVertex3fv(point + [fly_value])
        glEnd()
        glPopMatrix()
