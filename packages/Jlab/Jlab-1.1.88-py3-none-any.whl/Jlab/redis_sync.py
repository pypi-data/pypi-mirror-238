from os import listdir
from multiprocessing import Pool
from Jlab.utils import (
    get_github_repo,
    download_file,
    # get_file_list,
)
from retry import retry
from loguru import logger
import redis
import wget
import pickle
import os
import py7zr


class RedisSync:
    def __init__(self, db_channel):
        self.db_channel = db_channel

    # def restore(self, dataset):
    #    redis_conn = redis.Redis(host="127.0.0.1", port=6379, db=self.db_channel)
    #    with open(f"{dataset}.bin", "rb") as f:
    #        redis_conn.set(dataset.encode("utf-8"), f.read())
    #    redis_conn.close()

    def restore(self, redis_key, df_pickle):
        redis_conn = redis.Redis(host="127.0.0.1", port=6379, db=self.db_channel)
        redis_conn.set(redis_key, df_pickle)
        print(pickle.loads(redis_conn.get(redis_key)))
        redis_conn.close()

    def get_files(self):
        if not os.path.exists("finlab_database.csv"):
            self.wget_file(
                f"https://github.com/twfxjjbw/stockinfo/raw/main/finlab_database.csv"
            )
        with open("finlab_database.csv", "r") as f:
            finlab_db_list = f.read()
            return [item.strip() for item in finlab_db_list.split(",")]

    def delete_all_keys(self):
        redis_conn = redis.Redis(host="127.0.0.1", port=6379, db=self.db_channel)
        redis_conn.flushdb()
        redis_conn.close()

    @retry(exceptions=Exception, tries=3, delay=2, backoff=2)
    def wget_file(self, url):
        try:
            wget.download(url)
        except Exception as e:
            print(f"[ERROR] Failed to download {url}: {e}")
            raise e

    def check_update(self, dataset):
        redis_conn = redis.Redis(host="127.0.0.1", port=6379, db=self.db_channel)
        data_keys = redis_conn.keys()
        if dataset.encode("utf-8") in data_keys:
            if os.path.exists(f"{dataset}.7z"):
                os.remove(f"{dataset}.7z")

            self.wget_file(
                f"https://github.com/twfxjjbw/stockinfo/raw/main/{dataset}.7z"
            )
            folder = "pickles"
            with py7zr.SevenZipFile(f"{dataset}.7z", mode="r") as z:
                file_name = z.getnames()[0]
                z.extractall(path=folder)
                with open(folder + "/" + file_name, "rb") as f:
                    github_df = pickle.load(f)
                    if "date" in github_df.columns.to_list():
                        github_df.set_index("date", inplace=True)
                    local_df = pickle.loads(redis_conn.get(dataset))
                    if "date" in local_df.columns.to_list():
                        local_df.set_index("date", inplace=True)
                    redis_conn.close()
                    print("\n", local_df.index.to_list()[-1].strftime("%Y-%m-%d"))
                    if github_df.index.to_list()[-1].strftime(
                        "%Y-%m-%d"
                    ) == local_df.index.to_list()[-1].strftime("%Y-%m-%d"):
                        return False
        else:
            redis_conn.close()
        return True

    def download_and_restore(self, dataset):
        try:
            folder = "pickles"
            self.wget_file(
                f"https://github.com/twfxjjbw/stockinfo/raw/main/{dataset}.7z"
            )
            with py7zr.SevenZipFile(f"{dataset}.7z", mode="r") as z:
                file_name = z.getnames()[0]
                z.extractall(path=folder)
                if dataset == "inventory":
                    return
                with open(folder + "/" + file_name, "rb") as f:
                    df = pickle.load(f)
                    self.restore(dataset, df_pickle=pickle.dumps(df))
            os.remove(f"{dataset}.7z")
        except Exception as e:
            logger.exception(f"[ERROR] Failed to restore {dataset}: {e}")

    def sync_github_to_redis(self, force_download=False, dataset=None):
        if self.check_update("price:收盤價") or force_download or dataset:
            # self.delete_all_keys()
            if dataset:
                all_files = dataset
            else:
                all_files = self.get_files()
            print(all_files)
            if True:
                # Create a process pool with 5 processes
                pool = Pool(processes=5)
                pool.map(self.download_and_restore, all_files)
                # Close the pool and wait for all processes to complete
                pool.close()
                pool.join()
            else:
                for file in all_files:
                    self.wget_file(
                        f"https://github.com/twfxjjbw/stockinfo/raw/main/{file}.bin"
                    )
                    print(f" {file}")
                    self.restore(file.split(".")[0])

                for file_name in listdir("."):
                    if file_name.endswith(".bin"):
                        os.remove(file_name)


if __name__ == "__main__":
    redis_sync = RedisSync(db_channel=8)
    redis_sync.sync_github_to_redis(force_download=True)
