trigger_dict = {
                "resources": {
                    "counters": [],
                    "timers": []
                },
                "start": [
                    "State 0"
                ],
                "states": [
                    {
                        "conditions": [
                            {
                                "fields": [
                                    {
                                        "mask": 255,
                                        "match": 68,
                                        "offset": 0
                                    },
                                    {
                                        "mask": 15,
                                        "match": 1,
                                        "offset": 3
                                    },
                                    {
                                        "mask": 240,
                                        "match": 0,
                                        "offset": 7
                                    },
                                    {
                                        "mask": 15,
                                        "match": 0,
                                        "offset": 10
                                    },
                                    {
                                        "mask": 252,
                                        "match": 0,
                                        "offset": 11
                                    },
                                    {
                                        "mask": 255,
                                        "match": 227,
                                        "offset": 12
                                    },
                                    {
                                        "mask": 255,
                                        "match": 26,
                                        "offset": 13
                                    }
                                ],
                                "type": "tlp_data"
                            }
                        ],
                        "name": "State 0",
                        "onMatch": [
                            {
                                "type": "trigger"
                            }
                        ]
                    }
                ]
            }

start_dict =  {"channels":[{"capture":{"buffer":{"limit":7730941104,"trigger_position":100},"strong_compression":False,"tlp_truncation":0},"name":"dn.0","prefilter":{"dllp":{"ack":True,"nack":True,"pm_enter_l1":True,"pm_enter_l23":True,"pm_request_l1":True,"pm_request_ack":True,"vendor":True,"mrinit":True,"dlf":True,"nop":True,"mrinit_fc1":True,"mrinit_fc2":True,"mrupdate_fc":True,"initfc1_p":True,"initfc1_np":True,"initfc1_cpl":True,"initfc2_p":True,"initfc2_np":True,"initfc2_cpl":True,"updatefc_p":True,"updatefc_np":True,"updatefc_cpl":True},"os":{"ack":True,"nack":True,"pm_enter_l1":True,"pm_enter_l23":True,"pm_request_l1":True,"pm_request_ack":True,"vendor":True,"mrinit":True,"dlf":True,"nop":True,"mrinit_fc1":True,"mrinit_fc2":True,"mrupdate_fc":True,"initfc1_p":True,"initfc1_np":True,"initfc1_cpl":True,"initfc2_p":True,"initfc2_np":True,"initfc2_cpl":True,"updatefc_p":True,"updatefc_np":True,"updatefc_cpl":True,"skp":True,"cskp":True,"fts":True,"eios":True,"eieos":True,"sds":True,"eds":True,"ts1":True,"ts2":True},"error":{"ack":True,"nack":True,"pm_enter_l1":True,"pm_enter_l23":True,"pm_request_l1":True,"pm_request_ack":True,"vendor":True,"mrinit":True,"dlf":True,"nop":True,"mrinit_fc1":True,"mrinit_fc2":True,"mrupdate_fc":True,"initfc1_p":True,"initfc1_np":True,"initfc1_cpl":True,"initfc2_p":True,"initfc2_np":True,"initfc2_cpl":True,"updatefc_p":True,"updatefc_np":True,"updatefc_cpl":True,"skp":True,"cskp":True,"fts":True,"eios":True,"eieos":True,"sds":True,"eds":True,"ts1":True,"ts2":True,"8b_10b":True,"128b_130b":True},"cxl":{"ack":True,"nack":True,"pm_enter_l1":True,"pm_enter_l23":True,"pm_request_l1":True,"pm_request_ack":True,"vendor":True,"mrinit":True,"dlf":True,"nop":True,"mrinit_fc1":True,"mrinit_fc2":True,"mrupdate_fc":True,"initfc1_p":True,"initfc1_np":True,"initfc1_cpl":True,"initfc2_p":True,"initfc2_np":True,"initfc2_cpl":True,"updatefc_p":True,"updatefc_np":True,"updatefc_cpl":True,"skp":True,"cskp":True,"fts":True,"eios":True,"eieos":True,"sds":True,"eds":True,"ts1":True,"ts2":True,"8b_10b":True,"128b_130b":True,"io":True,"io_ieds":True,"cachemem":True,"cachemem_ieds":True,"null_ieds":True,"almp":True,"almp_ieds":True,"reserved":True},"cachemem":{"ack":True,"nack":True,"pm_enter_l1":True,"pm_enter_l23":True,"pm_request_l1":True,"pm_request_ack":True,"vendor":True,"mrinit":True,"dlf":True,"nop":True,"mrinit_fc1":True,"mrinit_fc2":True,"mrupdate_fc":True,"initfc1_p":True,"initfc1_np":True,"initfc1_cpl":True,"initfc2_p":True,"initfc2_np":True,"initfc2_cpl":True,"updatefc_p":True,"updatefc_np":True,"updatefc_cpl":True,"skp":True,"cskp":True,"fts":True,"eios":True,"eieos":True,"sds":True,"eds":True,"ts1":True,"ts2":True,"8b_10b":True,"128b_130b":True,"io":True,"io_ieds":True,"cachemem":True,"cachemem_ieds":True,"null_ieds":True,"almp":True,"almp_ieds":True,"reserved":True,"data_be":True,"llcrd_ack":True,"retry_idle":True,"retry_req":True,"retry_ack":True,"retry_frame":True,"ide_idle":True,"ide_start":True,"ide_tmac":True,"init_param":True}},"type":"data"},{"capture":{"buffer":{"limit":7730941104,"trigger_position":100},"strong_compression":False,"tlp_truncation":0},"name":"up.0","prefilter":{"dllp":{"ack":True,"nack":True,"pm_enter_l1":True,"pm_enter_l23":True,"pm_request_l1":True,"pm_request_ack":True,"vendor":True,"mrinit":True,"dlf":True,"nop":True,"mrinit_fc1":True,"mrinit_fc2":True,"mrupdate_fc":True,"initfc1_p":True,"initfc1_np":True,"initfc1_cpl":True,"initfc2_p":True,"initfc2_np":True,"initfc2_cpl":True,"updatefc_p":True,"updatefc_np":True,"updatefc_cpl":True},"os":{"ack":True,"nack":True,"pm_enter_l1":True,"pm_enter_l23":True,"pm_request_l1":True,"pm_request_ack":True,"vendor":True,"mrinit":True,"dlf":True,"nop":True,"mrinit_fc1":True,"mrinit_fc2":True,"mrupdate_fc":True,"initfc1_p":True,"initfc1_np":True,"initfc1_cpl":True,"initfc2_p":True,"initfc2_np":True,"initfc2_cpl":True,"updatefc_p":True,"updatefc_np":True,"updatefc_cpl":True,"skp":True,"cskp":True,"fts":True,"eios":True,"eieos":True,"sds":True,"eds":True,"ts1":True,"ts2":True},"error":{"ack":True,"nack":True,"pm_enter_l1":True,"pm_enter_l23":True,"pm_request_l1":True,"pm_request_ack":True,"vendor":True,"mrinit":True,"dlf":True,"nop":True,"mrinit_fc1":True,"mrinit_fc2":True,"mrupdate_fc":True,"initfc1_p":True,"initfc1_np":True,"initfc1_cpl":True,"initfc2_p":True,"initfc2_np":True,"initfc2_cpl":True,"updatefc_p":True,"updatefc_np":True,"updatefc_cpl":True,"skp":True,"cskp":True,"fts":True,"eios":True,"eieos":True,"sds":True,"eds":True,"ts1":True,"ts2":True,"8b_10b":True,"128b_130b":True},"cxl":{"ack":True,"nack":True,"pm_enter_l1":True,"pm_enter_l23":True,"pm_request_l1":True,"pm_request_ack":True,"vendor":True,"mrinit":True,"dlf":True,"nop":True,"mrinit_fc1":True,"mrinit_fc2":True,"mrupdate_fc":True,"initfc1_p":True,"initfc1_np":True,"initfc1_cpl":True,"initfc2_p":True,"initfc2_np":True,"initfc2_cpl":True,"updatefc_p":True,"updatefc_np":True,"updatefc_cpl":True,"skp":True,"cskp":True,"fts":True,"eios":True,"eieos":True,"sds":True,"eds":True,"ts1":True,"ts2":True,"8b_10b":True,"128b_130b":True,"io":True,"io_ieds":True,"cachemem":True,"cachemem_ieds":True,"null_ieds":True,"almp":True,"almp_ieds":True,"reserved":True},"cachemem":{"ack":True,"nack":True,"pm_enter_l1":True,"pm_enter_l23":True,"pm_request_l1":True,"pm_request_ack":True,"vendor":True,"mrinit":True,"dlf":True,"nop":True,"mrinit_fc1":True,"mrinit_fc2":True,"mrupdate_fc":True,"initfc1_p":True,"initfc1_np":True,"initfc1_cpl":True,"initfc2_p":True,"initfc2_np":True,"initfc2_cpl":True,"updatefc_p":True,"updatefc_np":True,"updatefc_cpl":True,"skp":True,"cskp":True,"fts":True,"eios":True,"eieos":True,"sds":True,"eds":True,"ts1":True,"ts2":True,"8b_10b":True,"128b_130b":True,"io":True,"io_ieds":True,"cachemem":True,"cachemem_ieds":True,"null_ieds":True,"almp":True,"almp_ieds":True,"reserved":True,"data_be":True,"llcrd_ack":True,"retry_idle":True,"retry_req":True,"retry_ack":True,"retry_frame":True,"ide_idle":True,"ide_start":True,"ide_tmac":True,"init_param":True}},"type":"data"},{"capture":{},"name":"sideband.0","prefilter":{"0":True,"1":True,"4":True,"5":True,"6":True,"7":True,"8":True,"9":True,"10":True,"11":True,"12":True,"13":True,"17":True,"30":True,"31":True},"type":"sideband"},{"enable":False,"name":"smbus.0","prefilter":{"addresses":[],"nacks":False},"type":"smbus"}],"mode":"trigger","recording":False,"trigger":[{"resources":{"counters":[],"timers":[]},"start":["State 0"],"states":[{"conditions":[{"fields":[{"mask":255,"match":68,"offset":0},{"mask":15,"match":1,"offset":3},{"mask":240,"match":0,"offset":7},{"mask":15,"match":0,"offset":10},{"mask":252,"match":0,"offset":11},{"mask":255,"match":227,"offset":12},{"mask":255,"match":26,"offset":13}],"type":"tlp_data"}],"name":"State 0","onMatch":[{"type":"trigger"}]}],"type":"data","link":0}],                           }