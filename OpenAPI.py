import requests
import json
from enum import Enum
import datetime, timedelta

class APIConnect(object):

    def __init__(self, endpoint="",cli_id="",source="",apiToken=""):
        self.API_ENDPOINT = endpoint
        self.clientID = cli_id
        self.src = source
        self.apiToken=apiToken
        self.apiKey=""
        self.orderMap  = {}
        self.posMap = {}
        self.timeout = 10
        self.exchSegArr = ["NSEEQ","NSEFO","NSECU","BSEEQ","BSEFO","BSECU","MCXCO","NCDEXCO"]
        self.prodArr = ["INTRADAY","MARGIN","CNC"]
        self.validArr = ["DAY","IOC"]

        msg = "Wrapper init"
        print(msg)

    def getSegment(seg):
        switcher = {"EQ":"E","FO":"D","CU":"C","CO":"M"}
        return switcher.get(seg,"nothing")
    
    def getExchSeg(self,exchSeg):
        switcher = {"NSEEQ":{"exch":"NSE","seg":"E"},"NSEFO":{"exch":"NSE","seg":"D"},
                    "NSECU":{"exch":"NSE","seg":"C"},"BSEEQ":{"exch":"BSE","seg":"E"},
                    "BSEFO":{"exch":"BSE","seg":"D"},"BSECU":{"exch":"BSE","seg":"C"},
                    "MCXCO":{"exch":"MCX","seg":"M"},"NCDEXCO":{"exch":"NCDEX","seg":"M"}
                    }
        return switcher.get(exchSeg,"nothing")
    
    def getProduct(self,prod):
        switcher = {"INTRADAY":"I","MARGIN":"M","CNC":"C"}
        return switcher.get(prod,"nothing")
    
    def getValidity(self,valid):
        switcher = {"DAY":"DAY","IOC":"IOC"}
        return switcher.get(valid,"nothing")
        
    def callAPI(self,url,params):
        print("callAPI url ==>%s" %(self.API_ENDPOINT+url))
        print("callAPI params ==>%s" % json.dumps(params))

        try:
            r = requests.post(url=self.API_ENDPOINT+url, data=params,timeout=self.timeout)
            # extracting response text
            response = r.content
            print("callAPI responseData ==>%s" %response)
        except requests.exceptions.Timeout:
            return json.loads(self.jsonify("error","API call timed out"))
        except Exception as e:
            print("callAPI exception api call-->",e)
        try:
            response = json.loads(response)
        except Exception as e:
            print("callAPI exception json parse-->",e)
            raise e
        return response
    
    def init(self,endpoint,cli_id,source):
        global API_ENDPOINT, clientID, src  # Access the global variables
        if self.isLengthNotZero(endpoint):
            API_ENDPOINT = endpoint
        if self.isLengthNotZero(cli_id):
            clientID=cli_id
        if self.isLengthNotZero(source):
            src = source

    def orderbook(self):
        data = {
        "entity_id": self.clientID,
        "token_id": self.apiToken,
        "source": self.src,
        "data": {
            "client_id": self.clientID
            }
        }
        
        response = self.callAPI("/OrderBook/index",str(data))
        
        returnData={}
        returnData["status"] = response["status"]
        if response["data"]:
            returnData["data"] = response["data"]

        if len(response["data"])!=0:
            for x in response["data"]:
                self.orderMap[str(x["order_no"])] = x
            print("orderMap==="+json.dumps(self.orderMap))
        
        return returnData
        
    ##### end orderbook #####


    def tradebook(self):
        data = {
        "entity_id": self.clientID,
        "token_id": self.apiToken,
        "source": self.src,
        "data": {
            "client_id": self.clientID
            }
        }
        
        response = self.callAPI("/TradeBook/index",str(data))
    
        returnData={}
        returnData["status"] = response["status"]
        if(response["status"]=="success"):
            returnData["data"] = response["data"]
        else:
            returnData["message"] = response["message"]
        
        return returnData
        
    ##### end tradebook #####


    def position(self):
        data = {
        "entity_id": self.clientID,
        "token_id": self.apiToken,
        "source": self.src,
        "data": {
            "client_id": self.clientID
            }
        }
        
        response = self.callAPI("/NetPosition/index",str(data))
        
        returnData={}
        returnData["status"] = response["status"]
        if(response["status"]=="success"):
            returnData["data"] = response["data"]
        else:
            returnData["message"] = response["message"]

        if len(response["data"])!=0:
            counter = 1
            for x in response["data"]:
                self.posMap[str(x["symbol"]+"-"+x["series"]+"-"+x["exchange"])] = x
            print("posMap==="+json.dumps(self.posMap))
        
        return returnData
        
        
    ##### end position #####


    def limits(self):
        data = {
        "entity_id": self.clientID,
        "token_id": self.apiToken,
        "source": self.src,
        "data": {
            "client_id": self.clientID
            }
        }
        
        response = self.callAPI("/FundLimit/index",str(data))
        
        returnData={}
        returnData["status"] = response["status"]
        if(response["status"]=="success"):
            returnData["data"] = response["data"]
        else:
            returnData["message"] = response["message"]
        
        return returnData
        
    ##### end limits #####

    def limit_details(self):
        data = {
        "entity_id": self.clientID,
        "token_id": self.apiToken,
        "source": self.src,
        "data": {
            "client_id": self.clientID
            }
        }
        
        response = self.callAPI("/FundLimit/limitDetails",str(data))
        
        returnData={}
        returnData["status"] = response["status"]
        if(response["status"]=="success"):
            returnData["data"] = response["data"]
        else:
            returnData["message"] = response["message"]
        
        return returnData
        
    ##### end limit details #####


    def margin_calculator(self,exch,segment,secid,txn_type,qty):
        
        if self.isLengthNotZero(exch)==False:
            return self.jsonify("error","Exchange field cannot be blank")
        
        if self.isLengthNotZero(segment)==False:
            return self.jsonify("error","Segment field cannot be blank")
        
        if self.isLengthNotZero(secid)==False:
            return self.jsonify("error","Security ID field cannot be blank")
        
        if self.isLengthNotZero(txn_type)==False:
            return self.jsonify("error","Txn type field cannot be blank")
        
        if self.isLengthNotZero(qty)==False:
            return self.jsonify("error","Quantity field cannot be blank")
        
        data = {
        "entity_id": self.clientID,
        "token_id": self.apiToken,
        "source": self.src,
        "data": {
            "exchange": exch,
            "segment": segment,
            "security_id": secid,
            "txn_type": txn_type,
            "Quantity": qty
            }
        }
        
        response = self.callAPI("/MarginCalc",str(data))
        
        returnData={}
        returnData["status"] = response["status"]
        if(response["status"]=="success"):
            returnData["data"] = response["data"]
        else:
            returnData["message"] = response["message"]
        
        return returnData
        
    ##### end margin calc #####


    def market_status(self,exch,segment):
        
        if self.isLengthNotZero(exch)==False:
            return self.jsonify("error","Exchange field cannot be blank")
        
        if self.isLengthNotZero(segment)==False:
            return self.jsonify("error","Segment field cannot be blank")
        
        data = {
        "entity_id": self.clientID,
        "token_id": self.apiToken,
        "source": self.src,
        "data": {
            "Exchange": exch,
            "Segment": segment,
            "mkt_type": ""
            }
        }
        
        response = self.callAPI("/MarketStatus/index",str(data))
        
        returnData={}
        returnData["status"] = response["status"]
        if(response["status"]=="success"):
            returnData["data"] = response["data"]
        else:
            returnData["message"] = response["message"]
        
        return returnData
        
    ##### end market status #####


    def trade_details(self,orderno,segment,legno):
        
        if self.isLengthNotZero(orderno)==False:
            return self.jsonify("error","Order No. field cannot be blank")
        
        if self.isLengthNotZero(segment)==False:
            return self.jsonify("error","Segment field cannot be blank")
        
        data = {
        "entity_id": self.clientID,
        "token_id": self.apiToken,
        "source": self.src,
        "data": {
            "client_id": self.clientID,
            "order_no": orderno,
            "segment": segment,
            "leg_no":legno
            }
        }
        
        response = self.callAPI("/TradeDetails/index",str(data))
        
        returnData={}
        returnData["status"] = response["status"]
        if(response["status"]=="success"):
            returnData["data"] = response["data"]
        else:
            returnData["message"] = response["message"]
        
        return returnData
        
    ##### end trade details #####


    def order_details(self,orderno="",segment=""):
        orderno = str(orderno)
        print("order_details==>"+orderno)
        # if(len(str(orderno))==0):
        #     return self.jsonify("error","Order No. field cannot be blank")
        
        if self.isLengthNotZero(orderno)==False:
            return self.jsonify("error","Order No. field cannot be blank")

        if(orderno not in self.orderMap):
            return self.jsonify("error","Invalid Order No.")
        
        orderObj = self.orderMap[orderno]
        
        data = {
        "entity_id": self.clientID,
        "token_id": self.apiToken,
        "source": self.src,
        "data": {
            "client_id": self.clientID,
            "order_no": orderno,
            "segment": orderObj["segment"]
            }
        }
        
        response = self.callAPI("/OrderDetails/index",str(data))
        
        returnData={}
        returnData["status"] = response["status"]
        if(response["status"]=="success"):
            returnData["data"] = response["data"]
        else:
            returnData["message"] = response["message"]
        
        return returnData
        
    ##### end trade details #####


    #def place_order(txn_type,exchange,segment,product,security_id,quantity,price,validity,disc_quantity,trigger_price,off_mkt_flag,good_till_days_date):
    def place_order(self,data):
        
        
        if self.isLengthNotZero(data["transaction_type"])==False:
            return self.jsonify("error","Txn Type field cannot be blank")
        
        if self.isLengthNotZero(data["exchange_segment"])==False:
            return self.jsonify("error","exchange_segment field cannot be blank")
        
        if self.isLengthNotZero(data["product"])==False:
            return self.jsonify("error","Product field cannot be blank")
        
        if self.isLengthNotZero(data["security_id"])==False:
            return self.jsonify("error","Sec id field cannot be blank")
        
        if self.isLengthNotZero(data["quantity"])==False:
            return self.jsonify("error","Quantity field cannot be blank")
        
        if self.isLengthNotZero(data["price"])==False:
            return self.jsonify("error","Price field cannot be blank")
        
        if self.isLengthNotZero(data["validity"])==False:
            return self.jsonify("error","Validity field cannot be blank")
        
        #if self.isLengthNotZero(data["disc_quantity"])==False:
         #   return self.jsonify("error","Disclose Qty field cannot be blank")
        
        #if self.isLengthNotZero(data["trigger_price"])==False:
        #    return self.jsonify("error","Trigger Price field cannot be blank")
        
        if self.isLengthNotZero(data["offline_order"])==False:
            return self.jsonify("error","Offline order field cannot be blank")
        
        #if length_check(data.period)==False:
        #    return jsonify("error","Price field cannot be blank")
        
        txn_type = data["transaction_type"]
        print("txntype==:%s" % type(data["transaction_type"]))

        txn_type = txn_type.upper()
        txn_type = "B" if txn_type=="BUY" else "S"

        exchSeg = data["exchange_segment"]
        exchSeg = self.getExchSeg(exchSeg)
        
        if isinstance(exchSeg, str):
            return self.jsonify("error","Invalid Exchange")
        
        exch = exchSeg["exch"]
        seg = exchSeg["seg"]
        
        prod = data["product"]
        prod = self.getProduct(prod)

        if prod=="nothing" :
            return self.jsonify("error","Invalid Product")
        
        validity = data["validity"]
        validity = self.getValidity(validity)

        if validity=="nothing" :
            return self.jsonify("error","Invalid Validity")
        
        iTrigPrc = 0
        iPrice=0
        trigprc = data["trigger_price"]
        if self.isLengthNotZero(trigprc) & isinstance(trigprc,str):
            iTrigPrc = float(trigprc)

        price = data["price"]
        if self.isLengthNotZero(price) & isinstance(price,str):
            iPrice = float(price)
        
        qty = data["quantity"]
        
        if isinstance(qty, str):
            qty = int(qty)
             
        ordtype = "LMT"
        if (iPrice!=0 & iTrigPrc==0):
            ordtype = "LMT"
        elif iPrice!=0 & iTrigPrc!=0:
            ordtype = "SL"
        elif iPrice==0 & iTrigPrc!=0:
            ordtype = "SLM"
        elif iPrice==0 & iTrigPrc==0:
            ordtype = "MKT"
            
        if(qty<1):
            return self.jsonify("error","Invalid Quantity")
            
        currdate = ""
        labelPeriod = "period"
        if labelPeriod in data:
            if self.isLengthNotZero(data["period"])==False:
                period = int(period)
                currdate = datetime.datetime.now()
                currdate = currdate + timedelta(days=period)
                currdate = currdate.strftime("%Y-%m-%d")
        
        
        orderdata = {
            "client_id": self.clientID,
            "user_id": self.clientID,
            "txn_type": txn_type,
            "exchange": exch,
            "segment":seg,
            "product":prod,
            "security_id":data["security_id"],
            "quantity":data["quantity"],
            "price":data["price"],
            "validity":data["validity"],
            "disc_quantity":data["disc_quantity"],
            "trigger_price":data["trigger_price"],
            "off_mkt_flag":data["offline_order"],
            "order_type":ordtype,
            "pro_cli":"C",
            "user_type":"C",
            "remarks":"",
            "mkt_type":"NL",
            "encash_flag":"false",
            "mkt_pro_flag":"N",
            "mkt_pro_value":"0",
            "good_till_days_date":currdate
            }
        
        data = {
        "entity_id": self.clientID,
        "token_id": self.apiToken,
        "source": self.src,
        "data": str(orderdata)
        }

        print("place_order object--> "+json.dumps(data))
        
        response = self.callAPI("/OrderEntry/index",str(data))
        
        print("place_order response-->",response)

        # returnData={}
        # returnData["status"] = response["status"]
        # if(response["status"]!="success"):
        #     returnData["message"] = response["message"]
        
        return response
        
    ##### end order entry #####


    def modify_order(self,data):
        
        if self.isLengthNotZero(data["quantity"])==False:
            return self.jsonify("error","Quantity field cannot be blank")
        
        if self.isLengthNotZero(data["price"])==False:
            return self.jsonify("error","Price field cannot be blank")
        
        if self.isLengthNotZero(data["validity"])==False:
            return self.jsonify("error","Validity field cannot be blank")
        
        # if self.isLengthNotZero(data["disc_quantity"])==False:
        #     return self.jsonify("error","Disclose Qty field cannot be blank")
        
        # if self.isLengthNotZero(data["trigger_price"])==False:
        #     return self.jsonify("error","Trigger Price field cannot be blank")
        
        if self.isLengthNotZero(data["order_id"])==False:
            return self.jsonify("error","Order id cannot be blank")

        orderdata = self.orderMap[data["order_id"]]
        if orderdata is None:
            return self.jsonify("error","Invalid Order id") 
        
        #if length_check(data["period)==False:
        #    return jsonify("error","Price field cannot be blank")
        
        validity = data["validity"]
        validity = self.getValidity(validity)

        if validity=="nothing" :
            return self.jsonify("error","Invalid Validity")
        
        iTrigPrc = 0
        iPrice=0
        trigprc = data["trigger_price"]
        if self.isLengthNotZero(trigprc) & isinstance(trigprc,str):
            iTrigPrc = float(trigprc)

        discqty = data["disc_quantity"]
        if self.isLengthNotZero(discqty) & isinstance(discqty,str):
            discqty = int(discqty)

        price = data["price"]
        if self.isLengthNotZero(price) & isinstance(price,str):
            iPrice = float(price)
        
        qty = data["quantity"]
        
        if isinstance(qty, str):
            qty = int(qty)
            
        ordtype = "LMT"
        if (iPrice!=0 & iTrigPrc==0):
            ordtype = "LMT"
        elif iPrice!=0 & iTrigPrc!=0:
            ordtype = "SL"
        elif iPrice==0 & iTrigPrc!=0:
            ordtype = "SLM"
        elif iPrice==0 & iTrigPrc==0:
            ordtype = "MKT"
            
        if(qty<1):
            return self.jsonify("error","Invalid Quantity")
            
        currdate = ""
        labelPeriod = "period"
        if labelPeriod in data:
            if self.isLengthNotZero(data["period"])==False:
                period = int(period)
                currdate = datetime.datetime.now()
                currdate = currdate + timedelta(days=period)
                currdate = currdate.strftime("%Y-%m-%d")
        
        
        orderdata = {
            "client_id": self.clientID,
            "user_id": self.clientID,
            "txn_type": orderdata["txn_type"],
            "exchange": orderdata["exchange"],
            "segment":orderdata["segment"],
            "product":orderdata["product"],
            "security_id":orderdata["security_id"],
            "quantity":data["quantity"],
            "price":data["price"],
            "validity":data["validity"],
            "disc_quantity":data["disc_quantity"],
            "trigger_price":data["trigger_price"],
            "off_mkt_flag":orderdata["off_mkt_flag"],
            "order_no":data["order_id"],
            "serial_no":orderdata["serial_no"],
            "order_type":ordtype,
            "pro_cli":"C",
            "user_type":"C",
            "remarks":"",
            "mkt_type":orderdata["mkt_type"],
            "mkt_pro_flag":orderdata["mkt_pro_flag"],
            "mkt_pro_value":orderdata["mkt_pro_value"],
            "good_till_days_date":currdate,
            
            "group_id":orderdata["group_id"],
            "remark1":"",
            "remark2":""
            }
        
        data = {
        "entity_id": self.clientID,
        "token_id": self.apiToken,
        "source": self.src,
        "data": str(orderdata)
        }
        
        
        response = self.callAPI("/OrderModify/index",str(data))
        
        # returnData={}
        # returnData["status"] = response["status"]
        # if(response["status"]=="success"):
        #     returnData["data"] = response["data"]
        # else:
        #     returnData["message"] = response["message"]
        
        return response
        
    ##### end order modify #####


    def cancel_order(self,data):
        
        if self.isLengthNotZero(data["order_id"])==False:
            return self.jsonify("error","Order id cannot be blank")

        orderdata = self.orderMap[data["order_id"]]
        if orderdata is None:
            return self.jsonify("error","Invalid Order id.")
        
        # txn_type = orderdata["txn_type"]
        # print("txntype==:%s" % type(data.transaction_type))
        
        orderdata = {
            "client_id": self.clientID,
            "user_id": self.clientID,
            "txn_type": orderdata["txn_type"],
            "exchange": orderdata["exchange"],
            "segment":orderdata["segment"],
            "product":orderdata["product"],
            "security_id":orderdata["security_id"],
            "quantity":orderdata["remaining_quantity"],
            "price":orderdata["price"],
            "validity":orderdata["validity"],
            "order_type":orderdata["order_type"],
            "disc_quantity":orderdata["disc_quantity"],
            "trigger_price":orderdata["trigger_price"],
            "off_mkt_flag":orderdata["off_mkt_flag"],
            "order_no":data["order_id"],
            "serial_no":orderdata["serial_no"],
        
            "pro_cli":"C",
            "user_type":"C",
            "remarks":"",
            "mkt_type":orderdata["mkt_type"],
            
            "mkt_pro_flag":orderdata["mkt_pro_flag"],
            "mkt_pro_value":orderdata["mkt_pro_value"],
            "good_till_days_date":orderdata["good_till_days_date"],
            
            "group_id":orderdata["group_id"],
            "remark1":"",
            "remark2":""
            }
        
        data = {
        "entity_id": self.clientID,
        "token_id": self.apiToken,
        "source": self.src,
        "data": str(orderdata)
        }
        
        response = self.callAPI("/OrderCancel/index",str(data))
        
        # returnData={}
        # returnData["status"] = response["status"]
        # if(response["status"]=="success"):
        #     returnData["data"] = response["data"]
        # else:
        #     returnData["message"] = response["message"]
        
        return response
        
    ##### end order cancel #####


    def convert_to_del(self,data):
        
        if self.isLengthNotZero(data["order_id"])==False:
            return self.jsonify("error","Order id cannot be blank")

        orderdata = self.orderMap[data["order_id"]]
        if orderdata is None:
            return self.jsonify("error","Invalid Order id.")
        
        
        
        #if length_check(data.period)==False:
        #    return jsonify("error","Price field cannot be blank")
        
        txn_type = orderdata["txn_type"]
        print("txntype==:%s" % type(data.transaction_type))
        
        data = {
            "client_id": self.clientID,
            "user_id": self.clientID,
            "txn_type": orderdata["txn_type"],
            "exchange": orderdata["Exchange"],
            "segment":orderdata["Segment"],
            "product":orderdata["Product"],
            "security_id":orderdata["security_id"],
            "quantity":orderdata["remaining_quantity"],
            "price":orderdata["Price"],
            "validity":orderdata["Validity"],
            "order_type":orderdata["order_type"],
            "disc_quantity":orderdata["disc_quantity"],
            "trigger_price":orderdata["trigger_price"],
            "off_mkt_flag":orderdata["off_mkt_flag"],
            "order_no":data.order_id,
            "serial_no":orderdata["serial_no"],
        
            "pro_cli":"C",
            "user_type":"C",
            "remarks":"",
            "mkt_type":orderdata["mkt_type"],
            
            "mkt_pro_flag":orderdata["mkt_pro_flag"],
            "mkt_pro_value":orderdata["mkt_pro_value"],
            "good_till_days_date":orderdata["good_till_days_date"],
            
            "group_id":orderdata["group_id"],
            "remark1":"",
            "remark2":""
            }
        
        
        response = self.callAPI("/ConvToDel/index",str(data))
        
        returnData={}
        returnData["status"] = response["status"]
        if(response["status"]=="success"):
            returnData["data"] = response["data"]
        else:
            returnData["message"] = response["message"]
        
        return returnData
        
    ##### end order cancel #####



    def isLengthNotZero(self,data):
        print ("isLengthNotZero==>"+data)
        return len(data)!=0

    ##### end length_check #####

    def jsonify(self,status,data):
        response={}
        response["status"] = status
        if status=="success":
            response["data"] = data
        else:
            response["message"] = data
        
        return json.dumps(response)

    ##### end jsonify #####

    def isValidExch(exch):
        match exch:
            case "NSE":
                return True
            case "BSE":
                return True
            case "MCX":
                return True
            case "NCDEX":
                return True
            case default:
                return False
            
    ##### end validateExch #####

    def getSegment(inst):
        match inst:
            case "EQUITY":
                return "E"
            case "FUTSTK":
                return "D"
            case "FUTIDX":
                return "D"
            case "FUTIVX":
                return "D"
            case "FUTCUR":
                return "C"
            case "OPTSTK":
                return "D"
            case "OPTIDX":
                return "D"
            case "OPTCUR":
                return "D"
            case "FUTCOM":
                return "M"
            case "OPTFUT":
                return "M"
            case default:
                return "E"
            
    ##### end validateExch #####

  

