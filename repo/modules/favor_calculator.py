import shutil
from ndn.encoding import TlvModel, BytesField

# class FavorParameterTypes:
#     RTT = 100
#     NETWORK_COST_PER_GB = 0.01
#     STORAGE_COST_PER_GB = 0.014
#     NUM_USERS = 100
#     BANDWIDTH = 25000 #Mbps
#     NETWORK_COST = NETWORK_COST_PER_GB * (BANDWIDTH/(1000*8)) #0.01 USD/GB  
#     RW_SPEED = 6.25
#     TOTAL_STORAGE, USED_STORAGE, REMAINING_STORAGE = shutil.disk_usage(__file__)
#     STORAGE_COST = REMAINING_STORAGE * STORAGE_COST_PER_GB

class FavorParameterTypes:
    RTT = 100
    NETWORK_COST_PER_GB = 200
    STORAGE_COST_PER_GB = 300
    NUM_USERS = 400
    BANDWIDTH = 500
    NETWORK_COST = 600
    RW_SPEED = 700
    TOTAL_STORAGE = 800
    USED_STORAGE = 900
    REMAINING_STORAGE = 1000
    STORAGE_COST = 1100

class FavorParameters(TlvModel):
    rtt = BytesField(FavorParameterTypes.RTT)
    num_users = BytesField(FavorParameterTypes.NUM_USERS)
    bandwidth = BytesField(FavorParameterTypes.BANDWIDTH)
    network_cost = BytesField(FavorParameterTypes.NETWORK_COST)
    storage_cost = BytesField(FavorParameterTypes.STORAGE_COST)
    remaining_storage = BytesField(FavorParameterTypes.REMAINING_STORAGE)

class FavorCalculator:
    """
    A class for abstracting favor calculations between two nodes.
    """
    def calculate_favor(self, favor_parameters: FavorParameters) -> float:
        favor = 0
        #for param, val in favor_parameters.asdict().items():
            # print(param, ':', val)
        #    favor += int(val)
        # print('favor:', favor)
        # favor = .3*FavorParameterTypes.REMAINING_STORAGE + .3*FavorParameterTypes.BANDWIDTH + .4*FavorParameterTypes.RW_SPEED + 0.0*FavorParameterTypes.NUM_USERS + 0.0*FavorParameterTypes.NETWORK_COST + 0.0*FavorParameterTypes.STORAGE_COST
        
        favor = 0.3*float(favor_parameters.remaining_storage) + 0.3*float(favor_parameters.bandwidth) + 0.4*float(favor_parameters.rtt) + 0.0*float(favor_parameters.num_users) + 0.0*float(favor_parameters.network_cost) + 0.0*float(favor_parameters.storage_cost)
        
        return favor
