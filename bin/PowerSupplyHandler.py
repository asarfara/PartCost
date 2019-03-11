import yaml, sys, logging

from sqlite3 import Error
from os.path import dirname, join, abspath
sys.path.append(abspath(join(dirname(__file__), '..')))

from src.Service.PriceChecker.PriceChecker import PriceChecker
from src.Service.PriceDatabaseBuilder.PriceDatabaseBuilder import PriceDatabaseBuilder
from src.Dao.Parts import Parts
from src.Service.DatabaseConnection.DatabaseConnection import DatabaseConnection

logger = logging.getLogger('PartCost')
logger.setLevel(logging.DEBUG)

file_handler = logging.FileHandler('/opt/projects/logs/app.log')
file_handler.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)

document = open('/opt/projects/config/powersupply.yaml', 'r')
database_file_name = "/opt/projects/db/parts.db"
partsList = yaml.safe_load(document)

databaseConnectionService = DatabaseConnection(database_file_name, logger)
priceChecker = PriceChecker(partsList, logger)

try:
    databaseConnection = databaseConnectionService.create_connection()

    priceDatabaseBuilder = PriceDatabaseBuilder(database_file_name, logger, databaseConnection)
    partsDao = Parts(database_file_name, logger, databaseConnection)

    priceDatabaseBuilder.create_table()
    partPrices = priceChecker.check_prices()
    partsDao.insert_parts(partPrices)
except Error as e:
    logger.error("Exception occurred in ProcessorHandler: {0}".format(e))
