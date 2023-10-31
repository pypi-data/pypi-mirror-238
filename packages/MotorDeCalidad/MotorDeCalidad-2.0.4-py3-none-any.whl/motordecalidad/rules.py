from typing import List
from pyspark.sql import DataFrame
from pyspark.sql.functions import (collect_list, concat_ws, current_date,
                                   datediff, expr, length, lit, mean,
                                   regexp_replace, split, stddev, sum, to_date,
                                   to_timestamp)
from pyspark.sql.window import Window
from motordecalidad.constants import *
from motordecalidad.utilities import *
from motordecalidad.functions import inform

#Function that validates if the DataFrame has data and has the required columns
def validateRequisites(object:DataFrame, field:list):
    fields = ','.join(field)
    error_list = list(set(field) - set(object.columns))
    rowsNumber = object.count()
    if len(error_list) == Zero and rowsNumber != Zero :
        inform("Ha superado la validación de requisitos exitosamente.\n")
        return (rowsNumber,Rules.Pre_Requisites.code,Rules.Pre_Requisites.name,Rules.Pre_Requisites.property,Rules.Pre_Requisites.code + "/" + fields,"100",PreRequisitesSucessMsg,fields,"100.00",0)
    elif len(error_list) != Zero:
        inform(f"Falta columna o la columna tiene un nombre distinto. Por favor chequear que el input tiene un esquema válido: {','.join(error_list)}")
        return (rowsNumber,Rules.Pre_Requisites.code,Rules.Pre_Requisites.name,Rules.Pre_Requisites.property,Rules.Pre_Requisites.code + "/" + fields,"100",f"Error en esquema de la tabla, revisar los siguientes campos: {','.join(error_list)}",fields,"0.00",rowsNumber)
    elif rowsNumber == Zero :
        inform("El dataframe de entrada no contiene registros")
        return (rowsNumber,Rules.Pre_Requisites.code,Rules.Pre_Requisites.name,Rules.Pre_Requisites.property,Rules.Pre_Requisites.code + "/" + fields,"100","DataFrame no contiene Registros",fields,"0.00",rowsNumber)

#Function that valides the amount of Null registers for certain columns of the dataframe
def validateNull(object:DataFrame,field: str,registersAmount: int,entity: str,threshold):
    dataRequirement = f"El atributo {entity}.{field} debe ser obligatorio (NOT NULL)."
    errorDf = object.filter(col(field).isNull())
    nullCount = object.select(field).filter(col(field).isNull()).count()
    notNullCount = registersAmount - nullCount
    ratio = (notNullCount/ registersAmount) * OneHundred
    return [registersAmount,Rules.NullRule.code,Rules.NullRule.name,Rules.NullRule.property,Rules.NullRule.code + "/" + entity + "/" + field,threshold,dataRequirement,field,ratio,nullCount], errorDf

#Function that valides the amount of Duplicated registers for certain columns of the dataframe
def validateDuplicates(object:DataFrame,fields:List,registersAmount: int,entity: str,threshold: int, repetitionsNumber = 1):
    windowSpec = Window.partitionBy(fields)
    fieldString = ','.join(fields)
    dataRequirement = f"Todos los identificadores {entity}.({fieldString}) deben ser distintos (PRIMARY KEY)."
    errorDf = object.withColumn("sum",sum(lit(One)).over(windowSpec)).filter(col("sum")>repetitionsNumber).drop("sum")
    nonUniqueRegistersAmount = errorDf.count()
    uniqueRegistersAmount = registersAmount - nonUniqueRegistersAmount
    ratio = (uniqueRegistersAmount / registersAmount) * OneHundred
    return [registersAmount,Rules.DuplicatedRule.code,Rules.DuplicatedRule.name,Rules.DuplicatedRule.property,Rules.DuplicatedRule.code + "/" + entity + "/" + fieldString,threshold,dataRequirement,fieldString,ratio,nonUniqueRegistersAmount], errorDf

#Function that valides the equity between certain columns of two objects
def validateReferentialIntegrity(
    testDataFrame: DataFrame,
    referenceDataFrame: DataFrame,
    testColumn: List,
    referenceColumn: List,
    registersAmount: int,
    entity: str,
    referenceEntity: str,
    threshold):
    fieldString = ','.join(testColumn)
    referenceFieldString = ','.join(referenceColumn)
    dataRequirement = f"El atributo {entity}.({fieldString}) debe ser referencia a la tabla y atributo {referenceEntity}.({referenceFieldString}) (FOREIGN KEY)."
    errorDf = testDataFrame.join(referenceDataFrame.select(referenceColumn).toDF(*testColumn), on = testColumn, how = LeftAntiType)
    errorCount = errorDf.count()
    ratio = (One - errorCount/registersAmount) * OneHundred
    return [registersAmount,Rules.IntegrityRule.code,Rules.IntegrityRule.name,Rules.IntegrityRule.property,Rules.IntegrityRule.code + "/" + entity + "/" + fieldString,threshold,dataRequirement,fieldString,ratio, errorCount], errorDf

#Function that validates if a Date Field has the specified Date Format
def validateFormatDate(object:DataFrame,
    formatDate:str,
    columnName:str,
    entity:str,  
    threshold,spark):
    notNullDf = object.filter(col(columnName).isNotNull())
    registerAmount = notNullDf.count()
    dataRequirement = f"El atributo {entity}.{columnName} debe tener el formato {formatDate}."
    spark.sql("set spark.sql.legacy.timeParserPolicy=LEGACY")
    if formatDate in DateFormats:
        errorDf = notNullDf.withColumn("output", to_date(col(columnName).cast('string'), formatDate))\
        .filter(col("output").isNull()).drop("output")
    elif formatDate in TimeStampFormats:
        errorDf = notNullDf.withColumn("output", to_timestamp(col(columnName).cast('string'), formatDate))\
        .filter(col("output").isNull()).drop("output")
    errorCount = errorDf.count()
    try:
        ratio = (One - errorCount/registerAmount) * OneHundred
    except:
        ratio = 100.0
    return [registerAmount,Rules.FormatDate.code,Rules.FormatDate.name + " - " + formatDate,Rules.FormatDate.property,Rules.FormatDate.code + "/" + entity + "/" + columnName,threshold,dataRequirement,columnName,ratio, errorCount], errorDf

#Function that validates if the data is between an specified range
def validateRange(object:DataFrame,
    columnName:str,
    registerAmount:int,
    entity:str,
    threshold:int,
    minRange = "",
    maxRange = "",
    includeLimitRight:bool = True,
    includeLimitLeft:bool = True,
    inclusive:bool = True,):
    dataRequirement =  f"El atributo {entity}.{columnName}, debe estar entre los valores {minRange} y {maxRange}"
    opel,opeg=chooseComparisonOparator(includeLimitLeft,includeLimitRight,inclusive)
    if minRange in object.columns:
        minRange = col(minRange)
    if maxRange in object.columns:
        maxRange = col(maxRange)

    if inclusive:
        if (minRange == "") and (maxRange != ""):
            errorDf = object.filter(opeg(col(columnName),maxRange))
        elif (minRange != "") and (maxRange == ""):
            errorDf = object.filter(opel(col(columnName), minRange))
        else: 
            errorDf = object.filter(opel(col(columnName),minRange) | opeg(col(columnName),maxRange))       
    else:
        errorDf = object.filter(opel(col(columnName),minRange) & opeg(col(columnName),maxRange))

    errorCount = errorDf.count()
    ratio = (One - errorCount/registerAmount) * OneHundred

    return [registerAmount,Rules.RangeRule.code,Rules.RangeRule.name,Rules.RangeRule.property,Rules.RangeRule.code + "/" + entity + "/" + columnName,threshold,dataRequirement, columnName, ratio, errorCount], errorDf

#Functions that validetes if the valus of a Column are contained in a set of permitted values
def validateCatalog(object:DataFrame,
    columnName:str, 
    registerAmount:int,
    entity:str,
    threshold: int,
    listValues:list):
    fieldsString = ','.join(listValues)
    dataRequirement = f"El atributo {entity}.{columnName}, debe tomar solo los valores {fieldsString}."
    evaluatedColumn = col(columnName).cast("string")
    errorDf = object.filter(~evaluatedColumn.isin(listValues))

    errorCount = errorDf.count()
    ratio = (One - errorCount/registerAmount) * OneHundred

    return [registerAmount,Rules.CatalogRule.code,Rules.CatalogRule.name,Rules.CatalogRule.property,Rules.CatalogRule.code + "/" + entity + "/" + columnName ,threshold,dataRequirement,columnName, ratio, errorCount], errorDf 
## Function that validates if the registers of a columna contain characters of a set of values
def validateForbiddenCharacters(object:DataFrame,
    columnName:str, 
    listValues:list,
    registerAmount:int,
    entity:str,
    threshold: int):

    fieldsString = ','.join(listValues)

    dataRequirement = f"El atributo {entity}.{columnName}, no debe contener los siguentes caracteres: {fieldsString}."

    vals="["+"".join(listValues)+"]"
    object = object.withColumn("replaced", regexp_replace(col(columnName),vals, ""))

    errorDf=object.filter(col(columnName)!=col('replaced')).drop('replaced')

    errorCount = errorDf.count()
    ratio = (One - errorCount/registerAmount) * OneHundred

    return [registerAmount, Rules.ForbiddenRule.code,Rules.ForbiddenRule.name,Rules.ForbiddenRule.property,Rules.ForbiddenRule.code + "/" + entity + "/" + columnName ,threshold,dataRequirement, columnName, ratio, errorCount], errorDf 
#Functions that validates thay the column is casteable to a data Type
def validateType(object:DataFrame,
    data_Type:str,
    columnName:str,
    registerAmount:int,
    entity:str,
    threshold: int):

    dataRequirement = f"El atributo {entity}.{columnName} debe ser de tipo {data_Type}."


    errorDf = object.filter(col(columnName).isNotNull()).withColumn("output", col(columnName).cast(data_Type))\
    .filter(col("output").isNull()).drop("output")

    errorCount = errorDf.count()
    ratio = (One - errorCount/registerAmount) * OneHundred
    return [registerAmount, Rules.Type.code, Rules.Type.name + " - " + data_Type, Rules.Type.property, Rules.Type.code + "/" + entity + "/" + columnName,threshold,dataRequirement,columnName,ratio, errorCount], errorDf

##Function that validates that a column is built out of the union of two other columns
def validateComposision(object: DataFrame,
    columnName:str,
    partialColumns:list,
    registerAmount:int,
    entity: str,
    threshold: int):

    fieldsString = ','.join(partialColumns)
    dataRequirement = f"El atributo {entity}.{columnName} en todas las tablas tiene que tener la siguiente estructura {fieldsString}"
    errorDf = object.filter(col(columnName) != concat_ws("_",*partialColumns))
    errorCount = errorDf.count()
    ratio = (One - errorCount/registerAmount) * OneHundred

    return [registerAmount, Rules.Composision.code, Rules.Composision.name, Rules.Composision.property, Rules.Composision.code + "/" + entity + "/" + columnName,threshold,dataRequirement,columnName,ratio, errorCount], errorDf

##Function that validates that all the registers of a column have the maximun defined length
def validateLength(object:DataFrame,
    columnName:str,
    registerAmount:int,
    entity,
    threshold,
    minRange = "",
    maxRange = ""):

    dataRequirement =  f"El atributo {entity}.{columnName}, debe contener este numero de caracteres {minRange} y {maxRange}"

    opel,opeg = chooseComparisonOparator(True, True, True)

    if (minRange == "") and (maxRange != ""):
        errorDf = object.filter(opeg(length(col(columnName)), maxRange))
    elif (minRange != "") and (maxRange == ""):
        errorDf = object.filter(opel(length(col(columnName)), minRange))
    else: 
        errorDf = object.filter(opel(length(col(columnName)), minRange) | opeg(length(col(columnName)), maxRange))       

    errorCount = errorDf.count()
    ratio = (One - errorCount/registerAmount) * OneHundred

    return [registerAmount,Rules.LengthRule.code,Rules.LengthRule.name,Rules.LengthRule.property,Rules.LengthRule.code + "/" + entity + "/" + columnName,threshold,dataRequirement, columnName, ratio, errorCount], errorDf

##Function that validates if a column's data type is the specified one
def validateDataType(object:DataFrame,
    columnName:str,
    registerAmount:int,
    entity:str,
    threshold:int,
    data_Type:str):

    dataRequirement =  f"El atributo {entity}.{columnName}, debe ser de tipo {data_Type}"
    try:
        if str(object.schema[columnName].dataType) == data_Type:
            ratio = 100.0
            errorCount = 0
            
        else:
            ratio = 0.0
            errorCount = object.count()
    except:
        try:
            if str(object.schema[columnName.upper()].dataType) == data_Type:
                ratio = 100.0
                errorCount = 0
            
            else:
                ratio = 0.0
                errorCount = object.count()
        except:
            if str(object.schema[columnName.lower()].dataType) == data_Type:
                ratio = 100.0
                errorCount = 0
            
            else:
                ratio = 0.0
                errorCount = object.count()

    return [registerAmount, Rules.DataTypeRule.code,Rules.DataTypeRule.name,Rules.DataTypeRule.property,Rules.DataTypeRule.code + "/" + entity + "/" + columnName,threshold,dataRequirement, columnName, ratio, errorCount]

#validates if the registers of a numerical column comply with the maximo amount of integer and decimal digits
def validateFormatNumeric(object:DataFrame,
    columnName:str,
    registerAmount:int,
    entity:str,
    threshold:int,
    maxInt:int,
    numDec:int,
    sep:str='.'):

    dataRequirement =  f"El atributo {entity}.{columnName}, debe ser tener el siguiente formato numerico {maxInt} {sep} {numDec}"
    sep = '\\' + sep
    if(str(object.schema[columnName].dataType)!='StringType'):
        object=object.withColumn(columnName,col(columnName).cast('string'))
    object = object.withColumn("int_num",split(object[columnName],sep).getItem(0)).withColumn("dec_num",split(object[columnName],sep).getItem(1))
    errorDf1 = object.filter((col("int_num").rlike("[^0-9]"))|(col("dec_num").rlike("[^0-9]")))
    errorDf2 = object.filter(~(col("int_num").rlike("[^0-9]"))|~(col("dec_num").rlike("[^0-9]"))).filter(length(col("int_num"))>lit(maxInt)).filter(length(col("dec_num"))>lit(numDec))
    errorDf = errorDf1.union(errorDf2).drop("int_num").drop("dec_num")
    errorCount = errorDf.count()
    ratio = (One - errorCount/registerAmount) * OneHundred

    return [registerAmount, Rules.NumericFormatRule.code,Rules.NumericFormatRule.name,Rules.NumericFormatRule.property,Rules.NumericFormatRule.code + "/" + entity + "/" + columnName,threshold,dataRequirement, columnName, ratio, errorCount], errorDf

#Function that validates if a time type column is in a range of values
def validateTimeInRange(object:DataFrame,
                columnName:str,
                referenceDate:str,
                formatDate:str,
                diffUnit:str,
                registerAmount:int,
                entity:str,
                threshold:int,
                minRange = "" ,
                maxRange = "",
                includeLimitRight:bool = True,
                includeLimitLeft:bool = True,
                inclusive:bool = True
                ):
    
    AuxColumn = "aux"
    columnsName = object.columns
    referenceDateRequirement = referenceDate

    if referenceDate in columnsName:
        diff_days = datediff(to_date(col(referenceDate), formatDate), to_date(col(columnName), formatDate))
        
    else:

        if (referenceDate == 'hoy'):
            referenceDate = current_date()
        
        else:
            referenceDate = expr("to_date('" + referenceDate + "', '"+ formatDate +"')")

        diff_days = datediff(lit(referenceDate), to_date(col(columnName)))
    
    if diffUnit == 'YEAR':
        diff = diff_days / 365

    elif diffUnit == 'MONTH':
        diff = diff_days / 30

    elif diffUnit == 'DAYS':
        diff = diff_days
    
    df_filtered = object.withColumn(AuxColumn, diff)
    data, errorDf = validateRange(df_filtered,AuxColumn,registerAmount,entity,threshold,minRange,maxRange,includeLimitRight,includeLimitLeft,inclusive)
        
    errorDf = errorDf.drop(AuxColumn)
    errorCount = data[-One]
    ratio = data[-2]

    dataRequirement =  f"La diferencia de fechas entre {referenceDateRequirement} Y {columnName} en {diffUnit} no está en el rango propuesto de minRange: {minRange} y maxRange: {maxRange}."

    return [registerAmount,Rules.validateTimeInRange.code,Rules.validateTimeInRange.name,Rules.validateTimeInRange.property,Rules.validateTimeInRange.code + "/" + entity + "/" + columnName,threshold,dataRequirement, columnName, ratio, errorCount], errorDf

#Function that validates any previous function using a condition over the dataset
def validateConditional(object:DataFrame,
                        registerAmount:int,
                        condition:str,
                        filterLists:List[List[any]],
                        entity:str,
                        threshold:int,
                        qualityFunction:List[List[any]]):
    if condition == "NO":
        column, sign, value = filterLists[0]
        if sign == "in" or sign == "==":
            object = object.filter(col(column).isin(value))
        elif sign == "not in":
            object = object.filter(col(column) != value)
        elif sign == "is" and value == "Null":
            object = object.filter(col(column).isNull())
        elif sign == "is" and value == "NotNull":
            object = object.filter(col(column).isNotNull())
        else:
            operator = {
                ">": ">",
                "<": "<",
            }.get(sign)
            filter_expr = expr(f"{column} {operator} {value}")
            object = object.filter(filter_expr)
    else:
        filters = []
        for filter_list in filterLists:
            column, sign, value = filter_list
            if sign == "in" or sign == "==":
                filters.append(col(column).isin(value))
            elif sign == "not in":
                filters.append(col(column) != value)
            elif sign == "is" and value == "Null":
                filters.append(col(column).isNull())
            elif sign == "is" and value == "NotNull":
                filters.append(col(column).isNotNull())
            else:
                operator = {
                    ">": ">",
                    "<": "<",
                }.get(sign)
                filter_expr = expr(f"{column} {operator} {value}")
                filters.append(filter_expr)
        if condition == "AND":
            condition_expr = filters[0]
            for i in range(1, len(filters)):
                condition_expr = condition_expr & filters[i]
        elif condition == "OR":
            condition_expr = filters[0]
            for i in range(1, len(filters)):
                condition_expr = condition_expr | filters[i]
        object = object.filter(condition_expr)
    registerAmount = object.count()
    functionName = qualityFunction[0]
    qualityFunction[2] = registerAmount
    qualityFunction[3] = entity
    qualityFunction[4] = threshold
    functionParameters = qualityFunction[1:]
    columnName = qualityFunction[1]
    applyFunction = globals()[functionName]
    if registerAmount != 0:
        data, errorDf = applyFunction(object, *functionParameters)
        dataRequirement = f"Para la condición de {column} {sign} {value}. {data[-4]}"
        errorCount = data[-One]
        ratio = data[-2]
    elif registerAmount == 0:
        errorDf = object
        dataRequirement = f"Para la condición de {column} {sign} {value} no existen registros."
        errorCount = 0
        ratio = 100.0
    return [registerAmount,Rules.validateConditional.code,Rules.validateConditional.name,Rules.validateConditional.property,Rules.validateConditional.code + "/" + entity + "/" + columnName,threshold,dataRequirement, columnName, ratio, errorCount], errorDf

#Function that validates that the characters in an specific position of a register have a preseted value
def validatePositionValue(object:DataFrame,
                        columnName:str,
                        registerAmount:int,
                        entity:str,
                        threshold:int,
                        initialPosition:int,
                        finalPosition:int,
                        expectedValue:List[any]):

    subString = col(columnName).substr(initialPosition, finalPosition - initialPosition + 1)
    errorDf = object.filter(~subString.isin(expectedValue))

    errorCount = errorDf.count()
    ratio = (One - errorCount/registerAmount) * OneHundred

    dataRequirement =  f"El atributo {columnName} no posee el valor de {expectedValue} en la posicion {initialPosition},{finalPosition} de su cadena"

    return [registerAmount, Rules.validatePositionValue.code, Rules.validatePositionValue.name, Rules.validatePositionValue.property, Rules.validatePositionValue.code + "/" + entity + "/" + columnName,threshold,dataRequirement,columnName,ratio, errorCount], errorDf
##Functions that validates that the registers of a column are valid emails
def validateEmail(object:DataFrame,
                  columnName:str,
                  registerAmount:int,
                  entity:str,
                  threshold:int,
                  domainsPermitted:DataFrame,
                  columnDomainReference:str,
                  expressionForbidden:List[any]):
    domainsPermitted = domainsPermitted.select(columnDomainReference).rdd.flatMap(lambda x:x).collect()
    emailFormat = r'^[\w\.-]+@([\w-]+\.)+[\w]+$'
    errorDf = object.filter(
        ~(col(columnName).rlike(emailFormat) & 
        (split(object[columnName], '@')[1].isin(domainsPermitted) &
        ~split(object[columnName], '@')[0].isin(expressionForbidden)))
    )    
    errorCount = errorDf.count() 
    ratio = (One - errorCount/registerAmount) * OneHundred
    dataRequirement =  f"El atributo {columnName} no cumple con el formato establecido."
    return [registerAmount, Rules.validateEmail.code, Rules.validateEmail.name, Rules.validateEmail.property, Rules.validateEmail.code + "/" + entity + "/" + columnName,threshold,dataRequirement,columnName,ratio, errorCount], errorDf
#Function that validates that the column complys with a mathematic operation
def validateOperation(object:DataFrame,
                      columnName:str,
                      registerAmount:int,
                      entity:str,
                      threshold:int,
                      operator:str,
                      input:str,
                      error:float=0):

    cols=object.columns
    res=operation(object,input)
    res.show()

    dataRequirement =  f"El atributo {entity}.{columnName}, no cumple con la ecuacion {columnName}, {operator}, {input}"

    if (operator=='=='):
        err=abs(1-col(columnName)/col(res.columns[-1]))
        errorDf=res.filter(err>error)
    else:
        func=chooseOper(res[res.columns[-1]],operator)
        errorDf=res.filter(func(col(columnName),res[res.columns[-1]]))

    errorCount = errorDf.count()
    ratio = (One - errorCount/registerAmount) * OneHundred

    return [registerAmount, Rules.OperationRule.code,Rules.OperationRule.name,Rules.OperationRule.property,Rules.OperationRule.code + "/" + entity + "/" + columnName,threshold,dataRequirement, columnName, ratio, errorCount], errorDf.select(cols)
#Function that validates if the values of a column fit within a distribution
def validateValueTendency(registerAmount,object:DataFrame,column,method,entity,threshold):
    DataRequirement =  f"Los valores de la columna {entity}.{column} deben estar dentro de la tendencia medida con el método {method}"
    col_mean = object.select(mean(col(column))).collect()[0][0]
    std_dev = object.select(stddev(col(column))).collect()[0][0]
    if method == "chebyshev":
        k = Two
        l_bound = col_mean - k*std_dev
        u_bound = col_mean + k*std_dev
    else:
        l_bound = col_mean -std_dev
        u_bound = col_mean + std_dev
    filteredDf = object.filter((col(column)>l_bound) & (col(column)< u_bound))
    errorDf = object.exceptAll(filteredDf)
    errorCount = errorDf.count()
    ratio = (One - errorCount/registerAmount) * OneHundred
    return [registerAmount, Rules.validateValueTendency.code, Rules.validateValueTendency.name, Rules.validateValueTendency.property, Rules.validateValueTendency.code + "/" + entity + "/" + column,threshold,DataRequirement,column,ratio, errorCount], errorDf
#Function that validates general statistics of a column
def measuresCentralTendency(object:DataFrame, columns, spark):
    pivotCol='summary'
    modes=("Mode",)
    columnSchema = [pivotCol]+columns
    
    for i in columns:
        if str(object.schema[i].dataType) == 'BooleanType()':
            object = object.withColumn(i, object[i].cast('string'))
        
        modes=modes+(str(object.groupby(i).count().orderBy("count", ascending=False).first()[0]),)
        
    res=object.select(columns).summary('stddev','mean','min','1%','5%','10%','25%','50%','75%','90%','95%','max')
    modeData = [modes]
    modeDf = spark.createDataFrame(data = modeData,schema = columnSchema)

    res = res.union(modeDf)
    columnsValue = list(map(lambda x: str("'") + str(x) + str("',")  + str(x), columns))
    stackCols = ','.join(x for x in columnsValue)
    df_1 = res.selectExpr(pivotCol, "stack(" + str(len(columns)) + "," + stackCols + ")")\
            .select(pivotCol, "col0", "col1")
    final_df = df_1.groupBy(col("col0")).pivot(pivotCol).agg(concat_ws("", collect_list(col("col1"))))\
                    .withColumnRenamed("col0", pivotCol)
    
    final_df=final_df.withColumnRenamed('summary', 'CAMPOS')\
                        .withColumnRenamed('1%','P1')\
                        .withColumnRenamed('5%','P5')\
                        .withColumnRenamed('25%','P25')\
                        .withColumnRenamed('50%','MEDIANA')\
                        .withColumnRenamed('75%','P75')\
                        .withColumnRenamed('90%','P90')\
                        .withColumnRenamed('95%','P95')\
                        .withColumnRenamed('Mode', 'MODA')\
                        .withColumnRenamed('mean', 'MEDIA')\
                        .withColumnRenamed('stddev','DESVIACION ESTANDAR')\
                        .withColumnRenamed('min','MIN')\
                        .withColumnRenamed('max','MAX')
    
    return final_df