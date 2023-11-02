import cx_Oracle
import pandas as pd
from django.conf import settings

DATABASES = settings.DATABASES
DATABASES_APPS_MAPPING = settings.DATABASES_APPS_MAPPING


class DatabaseAppsRouter:
    def db_for_read(self, model, **hints):
        app_label = (
            model._meta.app_label
            if not "." in (a := model._meta.verbose_name)
            else a.split(".")[0]
        )
        if app_label in DATABASES_APPS_MAPPING:
            return DATABASES_APPS_MAPPING[app_label]
        return None

    def db_for_write(self, model, **hints):
        app_label = (
            model._meta.app_label
            if not "." in (a := model._meta.verbose_name)
            else a.split(".")[0]
        )
        if app_label in DATABASES_APPS_MAPPING:
            return DATABASES_APPS_MAPPING[app_label]
        return None

    def allow_relation(self, obj1, obj2, **hints):
        obj1_app_lable = (
            obj1._meta.app_label
            if not "." in (a := obj1._meta.verbose_name)
            else a.split(".")[0]
        )
        obj2_app_lable = (
            obj2._meta.app_label
            if not "." in (a := obj2._meta.verbose_name)
            else a.split(".")[0]
        )
        db_obj1 = DATABASES_APPS_MAPPING.get(obj1_app_lable)
        db_obj2 = DATABASES_APPS_MAPPING.get(obj2_app_lable)
        if db_obj1 and db_obj2:
            if db_obj1 == db_obj2:
                return True
            else:
                return False
        return None

    def db_for_migrate(self, db, app_label, model_name=None, **hints):
        if db in DATABASES_APPS_MAPPING.values():
            return DATABASES_APPS_MAPPING.get(app_label) == db
        elif app_label in DATABASES_APPS_MAPPING:
            return False
        return None


class DBConfig:
    def __init__(self, tns_config):
        self.tns_config = tns_config

        self.initDBConfig()
        pass

    def runOracle(self):
        tns_config = self.tns_config

        user = tns_config.get("user")
        password = tns_config.get("password")
        host = tns_config.get("host")
        service_name = tns_config.get("service_name")
        sql_str = tns_config.get("sql_str")

        conn_str = f"{user}/{password}@{host}/{service_name}"  # ('system/system@172.24.0.64:1521/helowinXDB')

        conn = cx_Oracle.connect(conn_str)
        cursor = conn.cursor()
        cursor.execute(sql_str)
        col = [x[0] for x in cursor.description]
        qs = cursor.fetchall()
        cursor.close()  # 关闭游标
        conn.close()  # 关闭数据库连接

        if qs:
            data = []
            for i in qs:
                data.append(dict(zip(col, i)))
            return data
        else:
            return False

    def updateDBs(data):
        db_list = (
            pd.DataFrame(data)
            .groupby(["ENGINE_NAME", "ENGINE_CONTENT"])
            .apply(lambda x: x.to_dict("records"))
            .to_frame("MAPPING")
            .reset_index(drop=False)
            .to_dict("records")
        )

        if db_list:
            print("=" * 100)
            for i_index, i in enumerate(db_list):
                # update DATABASES
                DATABASES[i.get("ENGINE_NAME")] = eval(i.get("ENGINE_CONTENT"))
                print(
                    i_index,
                    " DATABASES Add success",
                    "=======> ",
                    '"' + str(i.get("ENGINE_NAME")) + '"',
                    ":",
                    i.get("ENGINE_CONTENT"),
                )
                if i["MAPPING"]:
                    for n_index, n in enumerate(i["MAPPING"]):
                        DATABASES_APPS_MAPPING[n.get("VERBOSE_ENGINE_NAME")] = i.get(
                            "ENGINE_NAME"
                        )
                        print(
                            "      ",
                            n_index,
                            "Mapping Add success",
                            "===> ",
                            '"' + str(n.get("VERBOSE_ENGINE_NAME")) + '"',
                            ":",
                            '"' + str(i.get("ENGINE_NAME")) + '"',
                        )
                        print("=" * 100)
            if not DATABASES.get("default"):
                DATABASES["default"] = {}
                DATABASES_APPS_MAPPING["default"] = "default"
        else:
            print("=" * 10)
            print("no database list found - by dbconfig")
            print("=" * 10)
        pass

    def initDBConfig(self):
        data = self.runOracle()
        if data:
            self.updateDBs(data)

        else:
            print("=" * 80)
            print("=====> no project detail found - by dbconfig")
            print("=" * 80)
