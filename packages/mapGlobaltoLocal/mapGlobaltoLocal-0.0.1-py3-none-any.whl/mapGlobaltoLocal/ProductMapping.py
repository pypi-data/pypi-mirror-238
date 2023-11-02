from pyspark.sql import SparkSession
spark = SparkSession.builder.appName("abc").getOrCreate()

df_bdl_global = spark.read.format("delta").load("/mnt/adls/centrallakePROD/BusinessDataLake/SC/Hierarchies/GlobalProductHierarchyLatest/Processed_Parquet/Global/")
df_bdl_global.createOrReplaceTempView('vw_bdl_hgpl')

class InvalidObjectErrorAtSKULevel(Exception):
  def __init__(self,message = 'Invalid Region name entered, suggested regions mapped at SKU Level: Fusion, Cordillera, Sirius, U2K2, SiriusVanguard'):
    self.message = message
    super().__init__(self.message)

def getMaterialMappedAtSKULevel(dataset):
  
  if dataset.casefold() == 'Sirius'.casefold():
    regionID = "E"
    path = "dbfs:/mnt/adls/centrallakePROD/BusinessDataLake/SC/Hierarchies/HierarchySiriusLocalProduct/Processed_Parquet/Sirius"

  elif dataset.casefold() == 'U2K2'.casefold():
    regionID = "R"
    path = "dbfs:/mnt/adls/centrallakePROD/BusinessDataLake/SC/Hierarchies/HierarchyU2K2LocalProduct/Processed_Parquet/U2K2"
  
  elif dataset.casefold() == 'Cordillera'.casefold():
    regionID = "A"
    path = "dbfs:/mnt/adls/centrallakePROD/BusinessDataLake/SC/Hierarchies/HierarchyCordilleraLocalProduct/Processed_Parquet/"

  elif dataset.casefold() == 'Fusion'.casefold():
    regionID = "I"
    path = "dbfs:/mnt/adls/centrallakePROD/BusinessDataLake/SC/Hierarchies/HierarchyFusionLocalProduct/Processed_Parquet/Fusion"

  elif dataset.casefold() == 'SiriusVanguard'.casefold():
    regionID = "E"
    path = "dbfs:/mnt/adls/centrallakePROD/BusinessDataLake/SC/Hierarchies/HierarchySiriusVanguardProduct/Processed_Parquet"
  
  else:
    raise InvalidObjectErrorAtSKULevel()
  
  data_local = spark.read.format("delta").load(path)
  data_local.createOrReplaceTempView('vw_udl_local')
    
  df = spark.sql(f"""Select B.RegionID as RegionID, A.SKUCODE as GlobalSKUCode, A.ProductName as GlobalSKUDescription, B.MaterialNumber as LocalMaterialCode, B.*
                  from vw_bdl_hgpl as A inner join vw_udl_local as B  
                  ON REPLACE(LTRIM(REPLACE(A.SKUCODE,'0',' ')),' ','0') = REPLACE(LTRIM(REPLACE(B.MaterialNumber,'0',' ')),' ','0') 
                  Where A.SKURegionID = '{regionID}'""")
  return df

def getMaterialMappedAtCPGLevel(dataset):
  a = "No Objects defined at present which can be mapped at CPG Level"
  return a

def getMaterialMappedAtBrandFormLevel(dataset):
  a = "No Objects defined at present which can be mapped at Brand Form Level"
  return a
  
