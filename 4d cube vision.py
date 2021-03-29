from manimlib.imports import *
import numpy as np


class Dot3D(Sphere):
	CONFIG = {"radius": 0.08,
	          "checkerboard_colors": [WHITE, WHITE],
	          "stroke_width": 0,
	          }


class FourDemention_Cube(ThreeDScene):
	CONFIG = {"x_axis_label": '$x$',
	          "y_axis_label": '$y$',
	          "z_axis_label": '$z$',
	          "camera_config": {"background_color": BLACK},
	          "dot_class": Dot3D,
	          "plane_use_ploygon": False,
	          }

	def construct(self):
		global j
		axes = ThreeDAxes()
		self.t = float(0)
		self.set_camera_orientation(phi=75 * DEGREES, theta=45 * DEGREES, distance=20)
		allpoint = [[-1, -1, -1, -1], [-1, -1, 1, -1], [-1, -1, 1, 1], [-1, -1, -1, 1], [-1, 1, -1, 1], [-1, 1, -1, -1],
		            [-1, 1, 1, -1], [-1, 1, 1, 1], [1, 1, 1, 1], [1, 1, -1, 1], [1, 1, -1, -1], [1, 1, 1, -1],
		            [1, -1, 1, -1], [1, -1, 1, 1],
		            [1, -1, -1, 1], [1, -1, -1, -1]]
		fourtothree_matrix = np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0]])
		point = []
		sphere = []
		Lines = []
		for i in range(16):
			sphere.append(self.dot_class().set_color(BLUE))
		index_line = []
		for i in range(16):
			for j in range(16):
				times = 0
				for k in range(4):
					if allpoint[i][k] == allpoint[j][k]: times += 1
				if times == 3:
					index_line.append([i, j])
		for i in index_line:
			for j in index_line:
				if i[1] == j[0] and i[0] == j[1]:
					index_line.remove(j)
		for j in range(32):
			Lines.append(Line())

		def fuc_of_vision(obj):
			return float(1/(2 - obj[3]))

		def Sphere4d_location(location):
			def Sphere4d(obj, dt):
				self.t += 0.05 * dt
				rotmatriYW = np.array([[1, 0, 0, 0],
				                       [0, np.cos(self.t), 0, -np.sin(self.t)],
				                       [0, 0, 1, 0],
				                       [0, np.sin(self.t), 0, np.cos(self.t)]])
				rotmatriZW = np.array([[1, 0, 0, 0],
				                       [0, 1, 0, 0],
				                       [0, 0, np.cos(self.t), -np.sin(self.t)],
				                       [0, 0, np.sin(self.t), np.cos(self.t)]])
				rotmatriXW = np.array([[np.cos(self.t), 0, 0, -np.sin(self.t)],
				                       [0, 1, 0, 0],
				                       [0, 0, 1, 0],
				                       [np.sin(self.t), 0, 0, np.cos(self.t)]])
				rotmatriXY = np.array([[np.cos(self.t), -np.sin(self.t), 0, 0],
				                       [np.sin(self.t), np.cos(self.t), 0, 0],
				                       [0, 0, 1, 0],
				                       [0, 0, 0, 1]])
				rotmatrixXZ = np.array([[np.cos(self.t), 0, -np.sin(self.t), 0],
				                        [0, 1, 0, 0],
				                        [np.sin(self.t), 0, np.cos(self.t), 0],
				                        [0, 0, 0, 1]], )
				rotmatrixYZ = np.array([[1, 0, 0, 0],
				                        [0, np.cos(self.t), -np.sin(self.t), 0],
				                        [0, np.sin(self.t), np.cos(self.t), 0],
				                        [0, 0, 0, 1]], )
				real_location = np.dot(rotmatriZW, np.dot(rotmatriXY, location, ))
				threedpoint = np.dot(fourtothree_matrix * fuc_of_vision(real_location), real_location)
				obj.move_to(threedpoint)

			return Sphere4d

		def Line4d_location(a, b):
			def Line4d(obj):
				obj.become(Line(a.get_center(), b.get_center()).set_color(WHITE))

			return Line4d

		for i in range(16):
			sphere[i].add_updater(Sphere4d_location(allpoint[i]))
		for i in range(32):
			Lines[i].add_updater(
				Line4d_location(sphere[int(index_line[i][0])], sphere[int(index_line[i][1])]))
		self.add(*[i for i in sphere], *[i for i in Lines], axes)
		self.wait(5)
