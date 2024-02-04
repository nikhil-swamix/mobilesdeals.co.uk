# import modin.pandas as dd
# import time
import csv
import glob
import json
import os
import re
import time
import tracemalloc
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
import pandas as pd
import requests
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv('../.env')
tracemalloc.start()

# sys.stdout = open('daemon-output.txt', 'w')


class Utils:
    def textsafe_pandasrow(row):
        '''Safely escape faulty characters'''
        result = []
        print(row)
        for c in row:
            try:
                if isinstance(c, str):
                    result.append(c.encode('windows-1252').decode('utf-8'))
                else:
                    result.append(c)
            except:
                result.append(c)

        return result

    def textsafe(cell):
        '''Safely escape faulty characters'''
        try:
            if isinstance(cell, str):
                return cell.encode('windows-1252').decode('utf-8')
            else:
                return cell
        except:
            return cell

    def tryjsonify(arg):
        try:
            return json.loads(arg)
        except:
            pass

    def chunk(xs, n):
        '''Split the list, xs, into n chunks'''
        L = len(xs)
        assert 0 < n <= L
        s = L // n
        return [xs[p : p + s] for p in range(0, L, s)]

    def reduce_products(common_name, collection):
        product = (
            collection.find_one({"common_name": common_name, "colour": "Black"})
            or collection.find_one({"common_name": common_name, "colour": "White"})
            or collection.find_one({"common_name": common_name, "colour": "Silver"})
            or collection.find_one({"common_name": common_name})
        )

        # find all docs matching common_name and get min value of Telcos%3Amonth_cost
        min_month_cost = (
            collection.find({"common_name": common_name}).sort("Telcos:month_cost", 1).limit(1)[0]["Telcos:month_cost"]
        )
        product["starting_monthly_price"] = min_month_cost
        return product


class Pipelines:
    def create_simple_catalog():
        """
        Create a single occurence unique collection from the MasterCatalog,
        by selecting one common_name for each product
        """
        # import TEXT
        from pymongo import TEXT

        master_collection = get_collection("MasterCatalog")
        print("Creating SimpleCatalog from MasterCatalog")
        common_names = master_collection.distinct("common_name")
        print(f"Found {len(common_names)} common_names")
        # get one product for each common_name
        with ThreadPoolExecutor(max_workers=8) as executor:
            products = [
                *executor.map(lambda common_name: Utils.reduce_products(common_name, master_collection), common_names)
            ]

        for product in products:
            print(product['common_name'], product['colour'])

        collection = get_collection("SimpleCatalog", drop=True)
        collection.insert_many(products)
        # create a text index
        collection.create_index([("common_name", TEXT)])


def split_csv_using_csv_module(csvpath, outpath="./pre/chunks", chunk_size=250):
    import zipfile

    """ read all files using glob
		if file is csv open directly
		if file is zip open zip file and read csv
		save the chunk to a file serially labelled
		1.makedirs if not exist
		2. finally save as zip file in outpath

	"""
    os.makedirs(outpath, exist_ok=True)
    # delete all files in outpath
    for file in os.listdir(outpath):
        os.remove(os.path.join(outpath, file))

    c = 0
    for p in glob.glob('./pre/*.csv.zip'):
        filename = os.path.basename(p).split('.')[0]  # equal to feed id
        try:
            for i, chunk in enumerate(pd.read_csv(p, encoding="utf-8", encoding_errors="ignore", chunksize=chunk_size)):
                chunk.to_csv(f'./pre/chunks/chunk{c}.csv', index=False)
                c += 1
        except Exception as e:
            print(f"Error: {e} in {filename}")
            continue


def downloader(url, filename):
    r = requests.get(url)
    open(
        filename,
        'wb',
    ).write(r.content)
    print(f"FILE: {filename}")
    return filename


def get_full_catalog():
    global VENDOR_IDS
    os.makedirs("pre", exist_ok=True)
    all_product_attrs = '''
	aw_deep_link, aw_product_id, aw_image_url,
	product_name, description, search_price,
	merchant_product_id, merchant_image_url, merchant_category, merchant_name, merchant_id,
	category_name, category_id,
	currency, store_price, delivery_cost,
	merchant_deep_link, language, last_updated,
	display_price, data_feed_id, brand_name, brand_id,
	colour, product_short_description, specifications,
	condition, product_model, model_number,
	dimensions, keywords, promotional_text,
	product_type, commission_group,
	merchant_product_category_path, merchant_product_second_category, merchant_product_third_category,
	rrp_price, saving, savings_percent,
	base_price, base_price_amount, base_price_text,
	product_price_old, delivery_restrictions, delivery_weight,
	warranty, terms_of_contract, delivery_time,
	in_stock, stock_quantity, valid_from, valid_to,
	is_for_sale, web_offer, pre_order,
	stock_status, size_stock_status, size_stock_amount,
	merchant_thumb_url, large_image, alternate_image,
	aw_thumb_url, alternate_image_two, alternate_image_three, alternate_image_four,
	reviews, average_rating, rating, number_available,
	custom_1, custom_2, custom_3, custom_4, custom_5, custom_6, custom_7, custom_8, custom_9,
	ean, isbn, upc, mpn,
	parent_product_id, product_GTIN, basket_link, Telcos%3Acontract_type,
	Telcos%3Aterm, Telcos%3Ainitial_cost, Telcos%3Amonth_cost,
	Telcos%3Agift, Telcos%3Ainc_minutes, Telcos%3Ainc_data,
	Telcos%3Aconnectivity, Telcos%3Ainc_texts, Telcos%3Atariff,
	Telcos%3Astorage_size, Telcos%3Aspecial_offer, Telcos%3Anetwork,
	Telcos%3Aoperating_system, Telcos%3Adevice_product_json,
	Telcos%3Adevice_product_version_json, Telcos%3Adevice_product_edition_json,
	Telcos%3Adevice_full_name, Telcos%3Adevice_description,
	Telcos%3Adevice_images_json, Telcos%3Adevice_features_json,
	Telcos%3Adevice_specifications_json, Telcos%3Anetwork_details_json,
	Telcos%3Atariff_group_details_json, Telcos%3Atariff_details_json,
	Telcos%3Atariff_allowances_json, Telcos%3Atariff_out_of_plan_charges_json,
	Telcos%3Adeal_tags_json, Telcos%3Adeal_type_json, Telcos%3Adeal_promo_info,
	Telcos%3Adeal_extras_json, Telcos%3Adeal_retailer_json, Telcos%3Adeal_cost_json,
	Telcos%3Adeal_discounts_json, Telcos%3Adeal_cashback_json,
	Telcos%3Adeal_legal_info, Telcos%3Asubscription_name, Telcos%3Asubscription_price_effective,
	Telcos%3Asubscription_renewal
	'''.replace(
        ' ', ''
    ).replace(
        '\n', ''
    )

    important_product_attrs = [
        "product_name",
        "colour",
        "brand_name",
        "aw_deep_link",
        "merchant_name",
        "merchant_category",
        "merchant_image_url",
        "merchant_thumb_url",
        "description",
        "Telcos%3Adevice_full_name",
        "Telcos%3Anetwork",
        "Telcos%3Agift",
        "Telcos%3Adevice_product_json",
        "Telcos%3Adevice_product_version_json",
        "Telcos%3Ainitial_cost",
        "Telcos%3Amonth_cost",
        "Telcos%3Atariff",
        "Telcos%3Ainc_minutes",
        "Telcos%3Ainc_texts",
        "Telcos%3Aconnectivity",
        "Telcos%3Ainc_data",
        "Telcos%3Astorage_size",
        # "Telcos%3Adevice_specifications_json",
        # "Telcos%3Adeal_extras_json",
        "Telcos%3Adeal_retailer_json",
        "Telcos%3Adeal_type_json",
        "Telcos%3Adeal_cost_json",
        "data_feed_id",
    ]
    # remove all csv.zip files from pre folder
    [os.remove(f) for f in glob.glob('./pre/*.csv.zip')]

    try:
        VENDOR_IDS = ADMIN_PANEL['VendorIdsList']
    except Exception as e:
        VENDOR_IDS = VENDOR_IDS
        print("LOG:VENDOR_IDS:IN_USE: ", VENDOR_IDS)

    API_KEY_FMOBILES = "d17a74eddb5293d5e7680cc0e67ff22d"
    VENDOR_URLS = [
        f'https://productdata.awin.com/datafeed/download/apikey/{API_KEY_FMOBILES}/language/en/fid/{VENDOR}/columns/{",".join(important_product_attrs)}/format/csv/delimiter/%2C/compression/zip/adultcontent/1/'
        for VENDOR in VENDOR_IDS
    ]
    VENDOR_FILES = [f'./pre/{VENDOR}.csv.zip' for VENDOR in VENDOR_IDS]

    if DEBUG:
        print("DEBUG:LOG: VENDOR_URLS", VENDOR_URLS)

    for k, v in zip(VENDOR_URLS, VENDOR_FILES):
        downloader(k, v)


def add_common_name(df):
    """add common_name column by joining product_name, colour, brand_name"""
    df = df.map(Utils.textsafe)
    n1 = df["Telcos:device_product_version_json"].apply(
        lambda x: json.loads(x),
    )

    n2 = df["Telcos:device_product_json"].apply(
        lambda x: json.loads(x),
    )

    df["common_name"] = (
        df["brand_name"]
        + n2.apply(lambda x: f' {x["product_name"]}')
        + n1.apply(lambda x: f' {x["product_version_name"]}')
    )

    cols = df.columns.tolist()
    cols.insert(1, cols.pop(cols.index('common_name')))
    df = df.loc[:, cols]  # reorder columns
    df = df[~df["merchant_category"].isin(["Mobile Phone", "SIM Card - PAYG"])]
    return df


def push_to_database(source=None, cli_mode=0):
    import pandas as pd

    """
			@panduram: if given then push pandas rows instead of using mongo import
			@reset: if True, Clears
			@cli_mode: its isdumb but fast, no scope for 2d json insert
			Import the merged multi vendor catalogue into MongoDB,
			download from here https://fastdl.mongodb.org/tools/db/mongodb-database-tools-windows-x86_64-100.6.1.msi
	"""
    collection = get_collection(COLLECTIONNAME)

    print("Processing source: ", source)

    # if type of source is a dataframe or path
    if isinstance(source, pd.DataFrame):
        pass
    elif isinstance(source, str):
        source = pd.read_csv(source)
    else:
        print("ERROR:LOG: source is not a dataframe or path to csv")
        return

    source = add_common_name(source)

    if not cli_mode:
        if source is not None:
            for col in source:
                if 'json' in col:
                    source[col] = source[col].apply(lambda x: Utils.tryjsonify(x))

            collection.insert_many(source.to_dict('records'))

    else:
        MASTERFILE = "master-data.csv"
        COMMAND = f"mongoimport --uri \"{connection_string}\" --collection {COLLECTIONNAME} --headerline --type CSV --file {MASTERFILE}"
        if DEBUG:
            print(COMMAND)
        else:
            os.system(COMMAND)


def get_collection(COLLECTIONNAME, drop=0):
    db = MongoClient(
        CONNSTRING,
    )[DBNAME]

    if drop:
        db[COLLECTIONNAME].drop()
        print(f"SUCCESS: {COLLECTIONNAME} HAS BEEN DROPPED")

    collection = db[COLLECTIONNAME]

    if collection is None:
        print(f"ERROR: {COLLECTIONNAME} NOT FOUND")
        return None
    return collection


def make_indexes(COLLECTIONNAME, attributes, reset=0):
    c = get_collection(COLLECTIONNAME)

    if reset:
        c.drop_indexes()

    if type(attributes) == str:
        attributes = [attributes]

    for attribute in attributes:
        c.create_index(attribute)
    print("INDEX CREATED", COLLECTIONNAME, attributes)


def unique_merchants_init():
    collection = get_collection("MasterCatalog")
    merchants = collection.distinct('merchant_name')
    # check if admin panel exists
    if not get_collection('AdminPanel').find_one({'identifier': "admin"}):
        get_collection('AdminPanel').insert_one({'identifier': "admin"})
    collection = get_collection('AdminPanel').update_one(
        {'identifier': "admin"},
        {'$set': {'MerchantNetworksList': [{'name': merchant, 'active': True} for merchant in merchants]}},
    )
    print(f"SUCCESS: {len(merchants)} MERCHANTS HAVE BEEN INITIALIZED", merchants)


class AdminPanel:
    def initialize():
        AdminPanel.update({'test': time.time()})

    def get():
        AP = 'AdminPanel'
        ID = {'identifier': "admin"}
        COL = get_collection(AP)

        result = COL.find_one(ID)
        if result is None:
            get_collection(AP).insert_one(ID)
            print("LOG: admin panel not found creating one")
            initialize()
            return get_collection(AP).find_one(ID)

        if COL.count_documents({}) == 0:
            get_collection(AP).insert_one(ID)
            return get_collection(AP).find_one(ID)

        print("LOG: AdminPanel: ", COL.find_one(ID))
        return COL.find_one(ID)

    def update(data):
        result = get_collection('AdminPanel').update_one({'identifier': "admin"}, {'$set': data})
        return result


def add_vendor_ids(VENDOR_IDS):
    ADMIN_PANEL = AdminPanel.get()
    ADMIN_PANEL.upadte({'VendorIdsList': VENDOR_IDS})


def set_pipeline_restart_progress(progress):
    ADMIN_PANEL = AdminPanel.get()
    if ADMIN_PANEL:
        ADMIN_PANEL['restart_progress'] = progress

    AdminPanel.update(ADMIN_PANEL)


def create_admin_password():
    AP = AdminPanel.get()
    if AP is not None:
        AP['password'] = "asdf1357"
        AdminPanel.update(AP)


def init_feed_merchant_map():
    """
    @: this is a one time function to initialize the merchant map
    USES: data_feed_id, merchant_name
    """
    mapper = {}
    C = get_collection(COLLECTIONNAME)
    # get distinct merchant_names
    merchants = C.distinct('merchant_name')
    print(merchants)
    for merchant in merchants:
        D = C.find_one({'merchant_name': merchant})
        if D is not None:
            print(D.get('data_feed_id'))
            if D.get('data_feed_id'):
                mapper[merchant] = D['data_feed_id']

    ADMIN_PANEL = AdminPanel.get()
    if ADMIN_PANEL:
        ADMIN_PANEL['FeedMerchantMap'] = mapper
        AdminPanel.update(ADMIN_PANEL)
        print("SUCCESS: FeedMerchantMap HAS BEEN INITIALIZED")


def main():
    print(f"Starting the master aggregation process @ {datetime.now()}")
    AdminPanel.get()
    set_pipeline_restart_progress(0)

    if os.path.exists('./database'):
        os.chdir('./database')

    AdminPanel.get()
    get_full_catalog()
    set_pipeline_restart_progress(5)

    if True:
        get_collection(COLLECTIONNAME).drop()
        print(COLLECTIONNAME, "Has been dropped")

    split_csv_using_csv_module('./pre', chunk_size=250)

    set_pipeline_restart_progress(30)

    print(glob.glob('./pre/chunks/*.csv'))

    P = ThreadPoolExecutor(8)
    P.map(push_to_database, glob.glob('./pre/chunks/*.csv'))
    P.shutdown(wait=True)
    set_pipeline_restart_progress(70)

    make_indexes(
        COLLECTIONNAME,
        [
            "merchant_name",
            "Telcos:network",
            "brand_name",
            "common_name",
            "colour",
            "Telcos:storage_size",
            "Telcos:deal_type_json.deal_type_name",
        ],
    )

    # Pipelines.create_simple_catalog()
    unique_merchants_init()
    init_feed_merchant_map()
    set_pipeline_restart_progress(100)


DEBUG = 0
DBNAME = os.getenv('DBNAME') or "mobilesdeals-co-uk"
CONNSTRING = os.getenv('MONGO_URI') or "mongodb://localhost:27017/"

COLLECTIONNAME = "MasterCatalog"
ADMIN_PANEL = AdminPanel.get()
VENDOR_IDS = ['18901', '11645', '11655', '11653', '33153', "13045"]


if __name__ == "__main__":
    # insert test doc
    # get_collection('MasterCatalogasdasd').insert_one({'test': 'test'})
    # get_full_catalog()
    # AdminPanel.initialize()

    # main()
    
    make_indexes(
        COLLECTIONNAME,
        [
            "merchant_name",
            "Telcos:network",
            "brand_name",
            "common_name",
            "colour",
            "Telcos:storage_size",
            "Telcos:deal_type_json.deal_type_name",
        ],
    )
    # print(os.getenv('MONGO_URI'))

    # unique_merchants_init()
    # split_csv_using_csv_module('./pre', chunk_size=500)

    # print(get_collection('AdminPanel').find_one({'identifier': "admin"}))
    # create_admin_password()

    # split_csv_using_csv_module('./pre', chunk_size=500)
    # m = pd.concat([pd.read_csv(f) for f in glob.glob('./pre/chunks/*.csv')], ignore_index=True)
    # print(m['merchant_category'].value_counts(), m.shape)

    # m = pd.concat([pd.read_csv(f) for f in glob.glob('./pre/*.csv.zip')], ignore_index=True)
    # print(m['merchant_category'].value_counts(), m.shape)

    # # db = MongoClient(CONNSTRING)[DBNAME]
    # # print(db.list_collection_names())

    print(list(map(lambda x: x / 1024 / 1024, tracemalloc.get_traced_memory())))
