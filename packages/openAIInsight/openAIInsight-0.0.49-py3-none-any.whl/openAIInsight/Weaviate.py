import weaviate
import json
import pandas as pd
import traceback
import datetime
from flask import request
import loggerutility as logger
import commonutility as common
from weaviate.gql.get import HybridFusion
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.retrievers.weaviate_hybrid_search import WeaviateHybridSearchRetriever
from langchain.schema import Document



class Weaviate:
    modelScope          =  "E"
    group_size          =  10000
    entity_type         =  ""
    schema_name         =  ""
    modelParameter      =  ""
    server_url          =  ""
    openAI_apiKey       =  ""
    enterpriseName      =  ""
    entity_type         =  ""
    docType_SchemaName  =  ""

    def traindata(self,weaviate_jsondata):
        try:
            logger.log(f'\n Print Weaviate start time for traning : {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}', "0")
            result                      = ""
            df                          = None
            columnnamelist              = []
            schemaClasslist             = []
            flag                        = ""
            propertyEmpty_flag          = "true"
            weaviate_IndexRespository   = []
            schemaName_Updated          = ""
            
            logger.log("inside Weaviate Hybrid class trainData()","0")
            logger.log(f"jsondata Weaviate Hybrid class trainData() ::: {weaviate_jsondata} ","0")
            if "openAI_apiKey" in weaviate_jsondata and weaviate_jsondata["openAI_apiKey"] != None:
                self.openAI_apiKey = weaviate_jsondata["openAI_apiKey"]           
                logger.log(f"\ntrain_Weaviate Hybrid openAI_apiKey:::\t{self.openAI_apiKey} \t{type(self.openAI_apiKey)}","0")
            
            if "modelParameter" in weaviate_jsondata and weaviate_jsondata["modelParameter"] != None:
                self.modelParameter = json.loads(weaviate_jsondata['modelParameter'])

            if "index_name" in self.modelParameter and (self.modelParameter["index_name"]).strip() != None:
                self.schema_name = (self.modelParameter["index_name"]).capitalize().replace("-","_").strip()
                logger.log(f"\ntrain_Weaviate Hybrid index_name:::\t{self.schema_name} \t{type(self.schema_name)}","0")

            elif "index_name" in weaviate_jsondata and (weaviate_jsondata["index_name"]).strip() != None:
                self.schema_name = (weaviate_jsondata["index_name"]).capitalize().replace("-","_").strip()
                logger.log(f"\ntrain_Weaviate Hybrid index_name:::\t{self.schema_name} \t{type(self.schema_name)}","0")

            if "entity_type" in self.modelParameter and (self.modelParameter["entity_type"]).strip() != None:
                self.entity_type = (self.modelParameter['entity_type']).lower().strip()
                logger.log(f'\n Tranin Weaviate vector entity_type veraible value :::  \t{self.entity_type} \t{type(self.entity_type)}')
            
            if "data_limit" in self.modelParameter and (self.modelParameter["data_limit"]).strip() != None and (self.modelParameter["data_limit"]).strip() != "":
                self.group_size = int(self.modelParameter['data_limit'])
                logger.log(f'\n Tranin Weaviate vector data_limit veraible value :::  \t{self.group_size} \t{type(self.group_size)}')

            if "modelScope" in weaviate_jsondata and weaviate_jsondata["modelScope"] != None:
                self.modelScope = weaviate_jsondata["modelScope"]
                logger.log(f"\ntrain_Weaviate class TrainData modelScope:::\t{self.modelScope} \t{type(self.modelScope)}","0")

            if "enterprise" in weaviate_jsondata and weaviate_jsondata["enterprise"] != None:
                self.enterpriseName = weaviate_jsondata["enterprise"]
                logger.log(f"\nWeaviate Hybrid class TrainData enterprise:::\t{self.enterpriseName} \t{type(self.enterpriseName)}","0")

            if "modelJsonData" in weaviate_jsondata and weaviate_jsondata["modelJsonData"] != None:
                self.dfJson = weaviate_jsondata["modelJsonData"]
            elif "dfJson" in weaviate_jsondata and weaviate_jsondata["dfJson"] != None:
                self.dfJson = weaviate_jsondata["dfJson"]
                logger.log(f"\ntrain_Weaviate Hybrid dfJson:::\t{self.dfJson} \t{type(self.dfJson)}","0")
            if type(self.dfJson) == str :
                parsed_json = json.loads(self.dfJson)
            else:
                parsed_json = self.dfJson

            if "server_url" in weaviate_jsondata and weaviate_jsondata["server_url"] != None:
                self.server_url = weaviate_jsondata["server_url"]
                logger.log(f"\nWeaviate Hybrid class TrainData server_url:::\t{self.server_url} \t{type(self.server_url)}","0")

            # Connection code with Weaviate
            client = weaviate.Client(self.server_url,additional_headers={"X-OpenAI-Api-Key": self.openAI_apiKey})

            logger.log(f'Connection is establish : {client.is_ready()}')

            if self.modelScope == "G" :
                self.enterpriseName = ""

            schemaName_Updated = self.enterpriseName + "_" + self.schema_name + "_" + self.entity_type
            logger.log(f'\nschemaName_Updated ::: \t{schemaName_Updated}')

            if self.schema_name == 'Document':
                logger.log(f"parsed_json::: {type(parsed_json)}\t{parsed_json}")
                copydict = parsed_json.copy()
                parsed_json = {"id" : 'String', "description" : 'String'}
                parsed_json.update(copydict[0]) # To add only document JSON Object 
                
                flag = self.documentTraining(client, parsed_json)
                
            
            else:
            # Schema Class parameter
                
                
                class_obj = {
                        "class": schemaName_Updated,
                        "vectorizer": "text2vec-openai",
                        "moduleConfig": {
                            "text2vec-openai": {},
                            "generative-openai": {}
                                        }
                            }
                # if schema is present then process should not create new one need to update
                weaviate_IndexRespository = client.schema.get()["classes"]
                schemaClasslist = [i['class'] for i in weaviate_IndexRespository]               
                
                if schemaName_Updated not in schemaClasslist:
                    client.schema.create_class(class_obj) # Schema Class Creation
                    logger.log(f"\n Schema: '{schemaName_Updated}' not present. Creating New !!!\n ")
                    
                    weaviate_IndexRespository = client.schema.get()["classes"]      # Updating variable value after new index creation
                    schemaClasslist = [i['class'] for i in weaviate_IndexRespository]  # Updating variable value after new index creation
                    logger.log(f"\nAvailable schema list::: {schemaClasslist} \n ")

                else:
                    logger.log(f"'{schemaName_Updated}' already present. Loading Now !!!\n ")
                
                for index, schemaObj in enumerate(weaviate_IndexRespository):
                    if schemaName_Updated == weaviate_IndexRespository[index]["class"]:
                        if not len(schemaObj["properties"])  > 0:
                            logger.log(f"Property empty for Weaviate Index '{schemaName_Updated}' case")
                            propertyEmpty_flag = "false"
                    else:
                        logger.log("Schema Name not present")

                if not schemaName_Updated == 'Document' :
                    if propertyEmpty_flag == "true" :
                        client.batch.delete_objects(class_name=schemaName_Updated,
                                                        where={'path': ["organization"],
                                                            'operator': 'Equal',
                                                            'valueText': str(self.enterpriseName) +"_"+ str(self.entity_type)
                                                },
                                            )
                        logger.log(f'\n {str(self.enterpriseName) +"_"+ str(self.entity_type)} against records are deleted ')
                    else:
                        logger.log(f'\n {schemaName_Updated} has no filter properties. Skipping records deletion.')

                columnnamelist=list(val for val in parsed_json[0])

                logger.log(f'\n Tranin Weaviate vector data_limit veraible value :::  \t{self.group_size} \t{type(self.group_size)}')

                num_groups = len(parsed_json[1:]) // self.group_size + (len(parsed_json[1:]) % self.group_size > 0)

                groups = []
                for i in range(num_groups):
                    start_idx = i * self.group_size
                    end_idx = (i + 1) * self.group_size if i < num_groups - 1 else len(parsed_json[1:])
                    group_indices = list(range(start_idx, end_idx))
                    groups.append(group_indices)

                logger.log(f'\n Print Weaviate Traning start time: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}', "0")
                logger.log(f'\n Number of Groups Created {len(groups)}', "0")

                for val in groups:
                    with client.batch.configure(batch_size=1000) as batch:
                        logger.log(f'\n Print Weaviate Group Traning start time: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}', "0")    
                        for indexvalue in val:          #  for each element of the list
                            if not indexvalue == 0:
                                properties = {
                                    "answer": parsed_json[indexvalue][columnnamelist[0]],
                                    "description": parsed_json[indexvalue][columnnamelist[1]],
                                    # "organization": str(self.enterpriseName) +"_"+ str(self.entity_type),
                                }
                                if len(columnnamelist) > 2:
                                    for j,valuedata in enumerate(columnnamelist[2:]):
                                        if valuedata not in parsed_json[indexvalue]:
                                            parsed_json[indexvalue][valuedata]=""
                                        else:
                                            properties[valuedata] = parsed_json[indexvalue][valuedata]
                                client.batch.add_data_object(
                                    properties,
                                    schemaName_Updated,
                                )
                        logger.log(f'\n Print Weaviate Group Traning END time: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}', "0")    
                        flag = "SUCCESSFUL"

            if flag == "SUCCESSFUL":
                result = f" {(schemaName_Updated if self.schema_name != 'Document' else self.docType_SchemaName)} Index Creation SUCCESSFUL. "
            else :
                result = f" {(schemaName_Updated if self.schema_name != 'Document' else self.docType_SchemaName)} Index Creation FAILED. "
            
            logger.log(f'\n Print Weaviate END time for traning : {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}', "0")
            logger.log(f" WEaviate Training final Result::: \n{result}\n ")
            return result
        except Exception as e:
            logger.log(f" {schemaName_Updated} Index Creation FAILED for Enterprise: '{self.enterpriseName}'. ","0")
            logger.log(f"{schemaName_Updated} class trainData() Issue::: \n{e}","0")
            trace = traceback.format_exc()
            descr = str(e)
            errorXml = common.getErrorXml(descr, trace)
            logger.log(f'\n {schemaName_Updated} class trainData() errorXml::: \n{errorXml}', "0")
            return str(errorXml)
        
    def getLookupData(self):
        
        try:
            logger.log(f'\n Print Weaviate start time for getLookupData : {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}', "0")
            logger.log("inside Weaviate Hybrid class LookUpData()","0")
            finalResultJson     =  {}
            id_list             =  []
            queryJson           =  ""
            schemaClasslist     =  []

            weaviate_json =  request.get_data('jsonData', None)
            weaviate_json = json.loads(weaviate_json[9:])
            logger.log(f"\nWeaviate hybrid class getLookupData() pineCone_json:::\t{weaviate_json} \t{type(weaviate_json)}","0")

            if "openAI_apiKey" in weaviate_json and weaviate_json["openAI_apiKey"] != None:
                self.openAI_apiKey = weaviate_json["openAI_apiKey"]          
                logger.log(f"\nWeaviate hybrid class LookUpData() openAI_apiKey:::\t{self.openAI_apiKey} \t{type(self.openAI_apiKey)}","0")              
            
            if "queryJson" in weaviate_json and weaviate_json["queryJson"] != None:
                queryJson = weaviate_json["queryJson"]
            elif "queryList" in weaviate_json and weaviate_json["queryList"] != None:
                queryJson = weaviate_json["queryList"]   
                logger.log(f"\nWeaviate hybrid class LookUpData() queryJson:::\t{queryJson} has length ::: '{len(queryJson)}'\t{type(queryJson)}","0")
            
            if "index_name" in weaviate_json and weaviate_json["index_name"] != None:
                self.schema_name = (weaviate_json["index_name"]).capitalize().replace("-","_")
                logger.log(f"\nWeaviate hybrid class LookUpData() schema_name:::\t{self.schema_name} \t{type(self.schema_name)}","0")

            if "enterprise" in weaviate_json and weaviate_json["enterprise"] != None:
                self.enterpriseName = weaviate_json["enterprise"]
                logger.log(f"\nWeaviate hybrid class LookUpData() enterprise:::\t{self.enterpriseName} \t{type(self.enterpriseName)}","0")

            if "server_url" in weaviate_json and weaviate_json["server_url"] != None:
                self.server_url = weaviate_json["server_url"]
                logger.log(f"\nWeaviate Hybrid class LookUpData server_url:::\t{self.server_url} \t{type(self.server_url)}","0")

            if "entity_type" in weaviate_json and weaviate_json["entity_type"] != None:
                self.entity_type = (weaviate_json['entity_type']).lower()
                logger.log(f'\n Tranin Weaviate vector entity_type veraible value :::  \t{self.entity_type} \t{type(self.entity_type)}')

            if "modelScope" in weaviate_json and weaviate_json["modelScope"] != None:
                self.modelScope = weaviate_json["modelScope"]
                logger.log(f"\nWeaviate hybrid class LookUpData() modelScope:::\t{self.modelScope} \t{type(self.modelScope)}","0")

            if self.modelScope == "G":
                self.enterpriseName = ""

            # Connection code with weaviate 

            client = weaviate.Client(self.server_url,additional_headers={"X-OpenAI-Api-Key": self.openAI_apiKey})

            schemaName_Updated = self.enterpriseName + "_" + self.schema_name + "_" + self.entity_type
            logger.log(f'\nschemaName_Updated ::: \t{schemaName_Updated}')
            schemaClasslist = [i['class'] for i in client.schema.get()["classes"]]               

            logger.log(f'Connection is establish : {client.is_ready()}')

            where_filter = {
                "path": ["organization"],
                "operator": "Equal",
                "valueText": str(self.enterpriseName) +"_"+ str(self.entity_type)
                            }
            
            if self.schema_name == 'Document':
                id_list = self.documentLookup(client , queryJson)
                # for key in queryJson:
                #     if len(queryJson[key]) > 0 and queryJson[key].strip() != "":
                #         response = (
                #                 client.query
                #                 .get(self.schema_name, ["description", "answer", "organization"])
                #                 .with_where(where_filter)
                #                 .with_hybrid(
                #                 alpha=1,
                #                 query=queryJson[key]
                #                 )
                #                 .with_additional('score')
                #                 .do()
                #                 )
                #         if response != {}:
                #             for i in response['data']['Get']['Document']:
                #                 if i["_additional"]['score'] > '0.016':
                #                     id_list.append(i['answer'])

                # logger.log(f"\n\n id_list:::{id_list} has length :::'{len(id_list)}' \t {type(id_list)}\n")
                finalResult = str(id_list)
                
            else:
                if schemaName_Updated in schemaClasslist:
                    for key in queryJson:
                        if len(queryJson[key]) > 0 and queryJson[key].strip() != "":
                            response = (
                                    client.query
                                    .get(schemaName_Updated, ["description", "answer"])     #,"organization"])
                                    # .with_where(where_filter)
                                    .with_hybrid(
                                        alpha=0.6,
                                        query=queryJson[key].upper().replace("N/A","").replace("."," ").replace(","," ").replace("-"," ").replace("_"," "),
                                        fusion_type=HybridFusion.RELATIVE_SCORE
                                    )
                                    .with_additional('score')
                                    .with_limit(1)
                                    .do()
                                    )
                            logger.log(f"responsee:::: {response}")
                            if response != {}:
                                finalResultJson[key]= {"material_description": response['data']['Get'][schemaName_Updated][0]['description'] , 
                                                                        "id": response['data']['Get'][schemaName_Updated][0]['answer']} if not "errors" in list(response.keys()) else response
                    
                    logger.log(f"\n\nfinalResultJson:::{finalResultJson} has length ::: '{len(finalResultJson)}' \t {type(finalResultJson)}\n")
                    finalResult = str(finalResultJson)
                else:
                    logger.log(f"Weaviate class getLookUP()::: \nIndex_Name: {schemaName_Updated} not found in weaviate_IndexList: {schemaClasslist}","0")
                    message = f"Index_Name: '{schemaName_Updated}' not found in weaviate_IndexList. \nAvailable IndexList: {schemaClasslist}"
                    errorXml = common.getErrorXml(message, "")
                    raise Exception(errorXml)

                logger.log(f'\n Print Weaviate END time for getLookupData : {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}', "0")
                logger.log(f'\n FINAL Result :::{finalResult}', "0")

            
            return finalResult
        except Exception as e:
            logger.log(f"Weaviate Hybrid class getLookUP() Issue::: \n{e}","0")
            trace = traceback.format_exc()
            descr = str(e)
            errorXml = common.getErrorXml(descr, trace)
            logger.log(f'\n Weaviate hybrid class getLookUP() errorXml::: \n{errorXml}', "0")
            raise str(errorXml)

    def documentTraining(self,client, parsedJson):
        logger.log(f"\nparsed Json::: \n{parsedJson}\n\n")
        logger.log(f'Connection is establish : {client.is_ready()}')
        
        self.docType_SchemaName = self.enterpriseName + "_" + self.schema_name 
        retriever               = ""
        
        retriever = WeaviateHybridSearchRetriever(
                                                    client      = client,
                                                    index_name  = self.docType_SchemaName,
                                                    text_key    = "text",
                                                    attributes  = [],
                                                    metadata    = {"metadata":"doc_id"},
                                                    create_schema_if_missing=True,
                                                )

        OCRText = list(json.loads(parsedJson["description"]).values())
        logger.log(f"OCRText::: \n{OCRText}\n\n{type(OCRText)} ")

        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)  # for txtFileObject
        texts = text_splitter.create_documents(OCRText)
        logger.log(f"texts - First 2 chunks::: \n{texts[:2]}\n Divided Chunks length:::\n{len(texts)} ")

        for i in range(len(texts)):
            texts[i].metadata["doc_id"] = str(parsedJson["id"]) + "__" + str(i)
        logger.log(f"\n\n--- Using Langchain approach --- \n\nTexts - Last 2 Chunks::: {texts[-2:]} {type(texts)}\n\n")

        retriever.add_documents(texts)
        logger.log(f"retriever::: {type(retriever)}\n retriever value::: \n{retriever}\n\n")
        if retriever != "":
            message = f"SUCCESSFUL"
        else:
            message = f"UNSUCCESSFUL"
        logger.log(f"Message:::\t Document training {message} for '{self.docType_SchemaName}' ")
        return message
        
    def documentLookup(self, client, queryJson):
        id_list             = set()
        chunkResponse_list  = set()
        docType_SchemaName  = self.enterpriseName + "_" + self.schema_name 

        retriever = WeaviateHybridSearchRetriever(
                                                    client      = client,
                                                    index_name  = docType_SchemaName,
                                                    text_key    = "text",
                                                    attributes  = ["doc_id"],
                                                    create_schema_if_missing = True,
                                                )
        
        for key in queryJson:
            
            if len(key) > 0 and key.strip() != "":
                logger.log(f"key::: {key}")
                response = retriever.get_relevant_documents(key)
                logger.log(f"\n\nResponse for query '{key}'::: {type(response)}\n{response}\n")

                if len(response) > 0 :
                    for result in response:
                        chunkResponse_list.add(result.page_content)
                        id_list.add(result.metadata['doc_id'])
                        
                    logger.log(f"\n\nid_list::: \t{id_list}\n\n Chunk Response::: \n{chunkResponse_list}\n\n")

                    id_list = [eachId[ : eachId.find("_")] if "_" in eachId else eachId for eachId in id_list ]
                    logger.log(f"After removing '_' id_list::: \t{id_list} {type(id_list)}")
                    id_list = list(id_list)
                    logger.log(f"After removing duplicates id_list::: \t{id_list} {type(id_list)}")
                    return id_list
                        

