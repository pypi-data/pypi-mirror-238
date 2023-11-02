#!/usr/bin/python3.9
# -*- coding: utf-8 -*-
# @Time    :  2022/10/28 18:56
# @Author  : chenxw
# @Email   : gisfanmachel@gmail.com
# @File    : gisTools.py
# @Descr   : 
# @Software: PyCharm

# !/usr/bin/python3.9
# -*- coding: utf-8 -*-
"""
    地理中经常使用的数学计算，把地球简化成了一个标准球形，若是想要推广到任意星球能够改为类的写法，而后修改半径便可
"""
import math
import re

import numpy as np
from osgeo import gdal
from osgeo import osr
from pyproj import Transformer


class GISHelper:
    earth_radius = 6370.856  # 地球平均半径，单位km，最简单的模型每每把地球当作完美的球形，这个值就是常说的RE
    math_2pi = math.pi * 2
    pis_per_degree = math_2pi / 360  # 角度一度所对应的弧度数，360对应2*pi

    def __init__(self):
        pass

    def lat_degree2km(self, dif_degree, radius=earth_radius):
        """
        经过圆环求法，纯纬度上，度数差转距离(km)，与中间点所处的地球上的位置关系不大
        :param dif_degree: 度数差, 经验值0.0001对应11.1米的距离
        :param radius: 圆环求法的等效半径，纬度距离的等效圆环是经线环，因此默认都是earth_radius
        :return: 这个度数差dif_degree对应的距离，单位km
        """
        return radius * dif_degree * self.pis_per_degree

    def lat_km2degree(self, dis_km, radius=earth_radius):
        """
        经过圆环求法，纯纬度上，距离值转度数(diff)，与中间点所处的地球上的位置关系不大
        :param dis_km: 输入的距离，单位km，经验值111km相差约(接近)1度
        :param radius: 圆环求法的等效半径，纬度距离的等效圆环是经线环，因此默认都是earth_radius
        :return: 这个距离dis_km对应在纯纬度上差多少度
        """
        return dis_km / radius / self.pis_per_degree

    def lng_degree2km(self, dif_degree, center_lat):
        """
        经过圆环求法，纯经度上，度数差转距离(km)，纬度的高低会影响距离对应的经度角度差，具体表达式为：
        :param dif_degree: 度数差
        :param center_lat: 中心点的纬度，默认22为深圳附近的纬度值；为0时表示赤道，赤道的纬线环半径使得经度计算和上面的纬度计算基本一致
        :return: 这个度数差dif_degree对应的距离，单位km
        """
        # 修正后，中心点所在纬度的地表圆环半径
        real_radius = self.earth_radius * math.cos(center_lat * self.pis_per_degree)
        return self.lat_degree2km(dif_degree, real_radius)

    def lng_km2degree(self, dis_km, center_lat):
        """
        纯经度上，距离值转角度差(diff)，单位度数。
        :param dis_km: 输入的距离，单位km
        :param center_lat: 中心点的纬度，默认22为深圳附近的纬度值；为0时表示赤道。
             赤道、中国深圳、中国北京、对应的修正系数分别约为： 1  0.927  0.766
        :return: 这个距离dis_km对应在纯经度上差多少度
        """
        # 修正后，中心点所在纬度的地表圆环半径
        real_radius = self.earth_radius * math.cos(center_lat * self.pis_per_degree)
        return self.lat_km2degree(dis_km, real_radius)

    def ab_distance(self, a_lat, a_lng, b_lat, b_lng):
        """
        计算经纬度表示的ab两点的距离，这是种近似计算，当两点纬度差距不大时更为准确，产生近似的缘由也是来主要自于center_lat
        :param a_lat: a点纬度
        :param a_lng: a点经度
        :param b_lat: b点纬度
        :param b_lng: b点纬度
        :return:
        """
        center_lat = .5 * a_lat + .5 * b_lat
        lat_dis = self.lat_degree2km(abs(a_lat - b_lat))
        lng_dis = self.lng_degree2km(abs(a_lng - b_lng), center_lat)
        return math.sqrt(lat_dis ** 2 + lng_dis ** 2)

    # # 构建矩形
    # def getPolyByRectCoords(self, coords):
    #     square = Polygon(
    #         ((coords[0], coords[2]), (coords[0], coords[3]), (coords[1], coords[3]), (coords[1], coords[2])))
    #     return square

    # 判断两个多边形是否相交
    # shaplely方法
    def isOverlap(self, poly1, poly2):
        return poly1.intersects(poly2) and not poly1.crosses(poly2) and not poly1.contains(poly2)

    # 通过经纬度得到像素坐标,根据地图高度宽度及地图经纬度范围
    def get_pixel_by_jwd(self, point_x: float, point_y: float, map_boundary: str, map_witdh: int,
                         map_height: int) -> str:
        minx = float(map_boundary.split(",")[0])
        miny = float(map_boundary.split(",")[1])
        maxx = float(map_boundary.split(",")[2])
        maxy = float(map_boundary.split(",")[3])
        # 通过地图长宽和经纬度坐标获取像素坐标
        pixel_x = map_witdh / (maxx - minx) * (point_x - minx)
        pixel_y = map_height / (maxy - miny) * (maxy - point_y)
        return round(pixel_x), round(pixel_y)

    # 通过中心点坐标，图片宽度，图片高度，分辨率得到图片四个点坐标,目前中心点坐标为经纬度
    def get_box_by_center(self, data_centerpt: str, data_resolution: float, data_image_width: int,
                          data_image_height: int) -> str:

        data_minx = float(data_centerpt.split(",")[0]) - self.lng_km2degree(
            float(data_image_width) / 2 * float(data_resolution) / 1000, float(data_centerpt.split(",")[1]))
        data_maxx = float(data_centerpt.split(",")[0]) + self.lng_km2degree(
            float(data_image_width) / 2 * float(data_resolution) / 1000, float(data_centerpt.split(",")[1]))
        data_miny = float(data_centerpt.split(",")[1]) - self.lat_km2degree(
            float(data_image_height) / 2 * float(data_resolution) / 1000, 6370.856)
        data_maxy = float(data_centerpt.split(",")[1]) + self.lat_km2degree(
            float(data_image_height) / 2 * float(data_resolution) / 1000, 6370.856)
        return data_minx, data_maxx, data_miny, data_maxy

    # 转换坐标---米到经纬度--多个点

    def convert_coords_array(self, request, *args, **kwargsst):
        try:
            res = ""
            # 参数1：坐标系WKID WGS_1984_UTM_Zone_54N 对应 32654
            # 参数2：WGS84地理坐标系统 对应 4326
            # 参数3: WGS84/UTM LJY,UTM无分带，强制对应为3857
            points = request.data.get("point")
            proj_txt = request.data.get("proj_txt").upper()
            center_lon = request.data.get("center_lon")
            center_lat = request.data.get("center_lat")
            self.logger.info("投影信息：{}".format(proj_txt))
            # 如果是经纬度，就不用转
            if proj_txt.strip().startswith("GEOGCS"):
                res = {}
                res["success"] = True
                body = {}
                body["point"] = points
                res["result"] = body
            else:
                proj = re.findall("PROJCS(.*?)GEOGCS", proj_txt)[0].lstrip("[")[:-1]
                epsg = self.get_utm_epsg(proj, center_lon, center_lat)
                self.logger.info("转换前的espg:{}".format(epsg))
                transformer = Transformer.from_crs("epsg:" + str(epsg), "epsg:4326")
                point_list = []
                for point in points:
                    x = point[0]
                    y = point[1]
                    lat, lon = transformer.transform(x, y)
                    point_list.append([lon, lat])
                res = {}
                res["success"] = True
                body = {}
                body["point"] = point_list
                res["result"] = body
        except Exception as exp:
            self.logger.error("坐标转换失败：" + str(exp))
            # 输出异常信息，错误行号等
            self.logger.info(exp)
            self.logger.info(exp.__traceback__.tb_frame.f_globals["__file__"])  # 发生异常所在的文件
            self.logger.info(exp.__traceback__.tb_lineno)  # 发生异常所在的行数
            res = {}
            res["success"] = False
            res["info"] = "坐标转换失败：" + str(exp)
        return res

        # 针对WGS_1984_UTM_Zone_57N这种WGS84 UTM的分带投影做坐标转换
        # 米到经纬度---单个点

    def convert_coords(self, request, *args, **kwargsst):
        try:
            res = ""
            point = request.data.get("point")
            point_x = point[0][0]
            point_y = point[0][1]
            proj_txt = request.data.get("proj_txt").upper()
            center_lon = request.data.get("center_lon")
            center_lat = request.data.get("center_lat")
            # 参数1：坐标系WKID WGS_1984_UTM_Zone_54N 对应 32654
            # 参数2：WGS84地理坐标系统 对应 4326
            # 如果是经纬度，就不用转
            if proj_txt.strip().startswith("GEOGCS"):
                res = {}
                res["success"] = True
                body = {}
                body["point"] = point
                res["result"] = body
            else:
                proj = re.findall("PROJCS(.*?)GEOGCS", proj_txt)[0].lstrip("[")[:-1]
                epsg = self.get_utm_epsg(proj, center_lon, center_lat)
                if epsg != -1:
                    self.logger.info("转换前的espg:{}".format(epsg))
                    transformer = Transformer.from_crs("epsg:" + str(epsg), "epsg:4326")
                    lat, lon = transformer.transform(point_x, point_y)
                    res = {}
                    res["success"] = True
                    body = {}
                    body["point"] = [[lon, lat]]
                    res["result"] = body
                else:
                    res = {}
                    res["success"] = False
                    res["info"] = "坐标转换失败，通过投影没有获取到EPSG，请检查数据"
        except Exception as exp:
            self.logger.error("坐标转换失败：" + str(exp))
            # 打印输出异常信息
            self.logger.info(exp)
            self.logger.info(exp.__traceback__.tb_frame.f_globals["__file__"])  # 发生异常所在的文件
            self.logger.info(exp.__traceback__.tb_lineno)  # 发生异常所在的行数
            # 生成返回结果
            res = {}
            res["success"] = False
            res["info"] = "坐标转换失败：" + str(exp)
        return res

        # 转换坐标---经纬度到米---多个点

    def convert_coords_array2(self, request, *args, **kwargsst):
        try:
            res = ""
            # 参数1：坐标系WKID WGS_1984_UTM_Zone_54N 对应 32654
            # 参数2：WGS84地理坐标系统 对应 4326
            points = request.data.get("point")
            proj_txt = request.data.get("proj_txt").upper()
            center_lon = request.data.get("center_lon")
            center_lat = request.data.get("center_lat")
            # 通过正则表达式得到坐标系
            # 投影1：PROJCS[\"WGS_1984_UTM_Zone_54N\",GEOGCS
            # 投影2：PROJCS[\"WGS 84 / UTM zone 54N\",GEOGCS
            proj = re.findall("PROJCS(.*?)GEOGCS", proj_txt)[0].lstrip("[")[:-1]
            epsg = self.get_utm_epsg(proj, center_lon, center_lat)
            self.logger.info("转换前的espg:{}".format(epsg))
            transformer = Transformer.from_crs("epsg:4326", "epsg:" + str(epsg))
            point_list = []
            # 循环坐标点数组
            for point in points:
                lon = point[0]
                lat = point[1]
                x, y = transformer.transform(lat, lon)
                point_list.append([x, y])
            res = {}
            res["success"] = True
            body = {}
            body["point"] = point_list
            res["result"] = body
        except Exception as exp:
            self.logger.error("坐标转换失败：" + str(exp))
            # 输出异常信息，错误行号等
            self.logger.info(exp)
            self.logger.info(exp.__traceback__.tb_frame.f_globals["__file__"])  # 发生异常所在的文件
            self.logger.info(exp.__traceback__.tb_lineno)  # 发生异常所在的行数
            res = {}
            res["success"] = False
            res["info"] = "坐标转换失败：" + str(exp)
        return res

        # 针对WGS_1984_UTM_Zone_57N这种WGS84 UTM的分带投影做坐标转换
        # 经纬度到米--单个点

    def convert_coords2(self, request, *args, **kwargsst):
        try:
            res = ""
            point = request.data.get("point")
            lon = point[0][0]
            lat = point[0][1]
            proj_txt = request.data.get("proj_txt").upper()
            center_lon = request.data.get("center_lon")
            center_lat = request.data.get("center_lat")
            # 参数1：坐标系WKID WGS_1984_UTM_Zone_54N 对应 32654
            # 参数2：WGS84地理坐标系统 对应 4326
            # 投影1：PROJCS[\"WGS_1984_UTM_Zone_54N\",GEOGCS
            # 投影2：PROJCS[\"WGS 84 / UTM zone 54N\",GEOGCS
            proj = re.findall("PROJCS(.*?)GEOGCS", proj_txt)[0].lstrip("[")[:-1]
            epsg = self.get_utm_epsg(proj, center_lon, center_lat)
            if epsg != -1:
                self.logger.info("转换前的espg:{}".format(epsg))
                # 建立转换器
                transformer = Transformer.from_crs("epsg:4326", "epsg:" + str(epsg))
                # lat, lon = transformer.transform(point_x, point_y)
                point_x, point_y = transformer.transform(lat, lon)
                res = {}
                res["success"] = True
                body = {}
                body["point"] = [[point_x, point_y]]
                res["result"] = body
            else:
                res = {}
                res["success"] = False
                res["info"] = "坐标转换失败，通过投影没有获取到EPSG，请检查数据"
        except Exception as exp:
            self.logger.error("坐标转换失败：" + str(exp))
            # 打印输出异常信息
            self.logger.info(exp)
            self.logger.info(exp.__traceback__.tb_frame.f_globals["__file__"])  # 发生异常所在的文件
            self.logger.info(exp.__traceback__.tb_lineno)  # 发生异常所在的行数
            # 生成返回结果
            res = {}
            res["success"] = False
            res["info"] = "坐标转换失败：" + str(exp)
        return res

        # 地理坐标系是球面,投影坐标系是平面;
        # 地理坐标系的单位为“度”,投影坐标系的单位为“米”;
        # 投影坐标(米)到地理坐标（度）

    def convert_coords_proj_2_geo(self, projection, x, y):
        pass
        prosrs = osr.SpatialReference()
        prosrs.ImportFromWkt(projection)
        geosrs = prosrs.CloneGeogCS()
        ct = osr.CoordinateTransformation(prosrs, geosrs)
        coords = ct.TransformPoint(x, y)
        # # 逆变换,实现投影到地理
        # p = Proj(projection)
        # lon, lat = p(x, y, inverse=True)
        return coords[:2][0], coords[:2][1]

        # 地理坐标（度）到投影坐标（米）

    def convert_coords_geo_2_proj(self, projection, lon, lat):
        pass
        prosrs = osr.SpatialReference()
        prosrs.ImportFromWkt(projection)
        geosrs = prosrs.CloneGeogCS()
        ct = osr.CoordinateTransformation(geosrs, prosrs)
        coords = ct.TransformPoint(lon, lat)
        return coords[:2][0], coords[:2][1]

        # 投影坐标（米）到投影坐标（米）

    def convert_coords_proj_2_proj(self, projection_source, projection_target, x, y):
        pass
        prosrs_source = osr.SpatialReference()
        prosrs_source.ImportFromWkt(projection_source)
        prosrs_target = osr.SpatialReference()
        prosrs_target.ImportFromWkt(projection_target)
        ct = osr.CoordinateTransformation(prosrs_source, prosrs_target)
        coords = ct.TransformPoint(x, y)
        return coords[:2][0], coords[:2][1]

    def convert_coords_list_by_wkt(self, request, convert_method, *args, **kwargsst):
        try:
            points = request.data.get("point")
            proj_txt = request.data.get("proj_txt")
            point_list = []
            # 循环坐标点数组
            for point in points:
                x = point[0]
                y = point[1]
                if convert_method == "proj_2_geo":
                    x_convert, y_convert = self.convert_coords_proj_2_geo(proj_txt, x, y)
                if convert_method == "geo_2_proj":
                    x_convert, y_convert = self.convert_coords_geo_2_proj(proj_txt, x, y)
                if convert_method == "proj_2_proj":
                    proj2_txt = request.data.get("proj2_txt")
                    x_convert, y_convert = self.convert_coords_proj_2_proj(proj_txt, proj2_txt, x, y)

                point_list.append([x_convert, y_convert])
            res = {}
            res["success"] = True
            body = {}
            body["point"] = point_list
            res["result"] = body
        except Exception as exp:
            self.logger.error("坐标转换失败：" + str(exp))
            # 输出异常信息，错误行号等
            self.logger.info(exp)
            self.logger.info(exp.__traceback__.tb_frame.f_globals["__file__"])  # 发生异常所在的文件
            self.logger.info(exp.__traceback__.tb_lineno)  # 发生异常所在的行数
            res = {}
            res["success"] = False
            res["info"] = "坐标转换失败：" + str(exp)
        return res

    def get_project_info(self, tiffile):
        projinfo = ""
        # dataset = gdal.open(tiffile)
        # projinfo = dataset.getProjection()
        return projinfo

        # 通过投影信息得到EPSG

    def get_utm_epsg(self, projection, center_lon, center_lat):
        epsg_code = -1
        try:
            self.logger.info("转换前的proj:{}".format(projection))
            utm_code = projection.replace(" ", "").replace("_", "").lower()
            # wgs84 utm分带投影的epsg计算
            if "utmzone" in utm_code and ("wgs84" in utm_code or "wgs1984" in utm_code):
                if len(re.findall("zone(.*?)n", utm_code)) > 0:
                    # 北半球 epsg=32600+wgs84 utm分度带号
                    utm_code_zone = int(re.findall("zone(.*?)n", utm_code)[0])
                    epsg_code = 32600 + utm_code_zone
                if len(re.findall("zone(.*?)s", utm_code)) > 0:
                    # 南半球 epsg=32700+wgs84 utm分度带号
                    utm_code_zone = int(re.findall("zone(.*?)s", utm_code)[0])
                    epsg_code = 32700 + utm_code_zone
            # utm没有分带投影的epsg计算
            elif "utm" in utm_code and "utmzone" not in utm_code:
                # 东半球
                if float(center_lon) > 0:
                    utm_code_zone = 31 + int(float(center_lon) / 6)
                # 西半球
                if float(center_lon) < 0:
                    utm_code_zone = 30 - int(abs(float(center_lon) / 6))
                # 北半球
                if float(center_lat) > 0:
                    epsg_code = 32600 + utm_code_zone
                # 南半球
                if float(center_lat) < 0:
                    epsg_code = 32700 + utm_code_zone

        except Exception as exp:
            self.logger.error("通过投影获取EPSG失败：" + str(exp))
            # epsg_code=3857
            self.logger.info(exp)
            self.logger.info(exp.__traceback__.tb_frame.f_globals["__file__"])  # 发生异常所在的文件
            self.logger.info(exp.__traceback__.tb_lineno)  # 发生异常所在的行数
        return int(epsg_code)

        # 计算多边形坐标的四至范围
        # 多边形坐标为[[point1x,point1y],[point2x,point2y],...[pointnx,pointny],[point1x,point1y]]

    # 计算多边形坐标的四至范围
    # 多边形坐标为[[point1x,point1y],[point2x,point2y],...[pointnx,pointny],[point1x,point1y]]
    @staticmethod
    def get_box_of_polygon_points(points):
        points_np = np.array(points)

        cols_min = np.min(points_np, axis=0)
        cols_max = np.max(points_np, axis=0)
        minx = cols_min[:1].tolist()[0]
        miny = cols_min[1:2].tolist()[0]
        maxx = cols_max[:1].tolist()[0]
        maxy = cols_max[1:2].tolist()[0]
        # minx = np.min(points_np[:, 0])
        # maxx = np.max(points_np[:, 0])
        # miny = np.min(points_np[:, 1])
        # maxy = np.max(points_np[:, 1])
        return minx, miny, maxx, maxy

    # # 投影坐标（米）转为地理坐标（经纬度）---方法暂时不可以用
    # def convert_coords2(self, sourceEPSG, x, y):
    #     pass
    #     # fromSRS = osr.SpatialReference()
    #     # fromSRS.ImportFromEPSG(sourceEPSG)
    #     # toSRS = osr.SpatialReference()
    #     # toSRS.SetWellKnownGeogCS("WGS84")
    #     # ct = osr.CoordinateTransformation(fromSRS, toSRS)
    #     # coords = ct.TransformPoint(x, y)
    #     # return coords[:2]
    #
    # # 得到tif文件的投影信息
    # def get_source_projection(self, tif_file):
    #     pass
    #     # dataset = gdal.Open(tif_file)
    #     # return dataset.GetProjection()
    #
    # # 投影坐标（米）转为地理坐标（经纬度）---方法可以用
    # def convert_coords(self, projection, x, y):
    #     pass
    #     # prosrs = osr.SpatialReference()
    #     # prosrs.ImportFromWkt(projection)
    #     # geosrs = prosrs.CloneGeogCS()
    #     # ct = osr.CoordinateTransformation(prosrs, geosrs)
    #     # coords = ct.TransformPoint(x, y)
    #     # return coords[:2]


if __name__ == '__main__':
    gisHelper = GISHelper()
    # print(gisHelper.lng_km2degree(0.5, 45))
    # dataset = gdal.Open("E:\\data\\123.tif")
    # print(dataset.GetProjection())
    # print(dataset.GetGeoTransform())

    print("---------------------------------")

    dataset = gdal.Open("E:\\data\\sar1234\\1234.tiff")
    print(dataset.GetProjection())
    print(dataset.GetGeoTransform())

    # 得到原始tif的投影信息
    # source_projection = gisHelper.get_source_projection("E:\\data\\123.tif")
    # source_projection = gisHelper.get_source_projection("E:\\desktop\\DEM\\ribenxibu.tif")
    # # 输入原始tif的投影信息，需要转换的点的投影坐标（米）
    # result = gisHelper.convert_coords(source_projection, 350388, 3957319.5)
    # # 输出 转换后的经纬度值（度）
    # print("lon:" + str(result[0]))
    # print("lat:" + str(result[1]))
