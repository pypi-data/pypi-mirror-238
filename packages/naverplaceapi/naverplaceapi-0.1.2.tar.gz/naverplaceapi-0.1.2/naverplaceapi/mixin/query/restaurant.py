# def create(businessId:str):
#     operation_name = "restaurant"
#     variables = _define_variables(businessId)
#     query = {
#         "operationName": operation_name,
#         "variables": variables,
#         "query": QUERY_STATEMENT
#     }
#     return query
#
#
# def _define_variables(businessId:str):
#     return {
#         "deviceType":"pcmap",
#         "id":businessId,
#         "isNx":False
#     }
#
#
# QUERY_STATEMENT = """query restaurant(
#                         $input: RestaurantsInput
#                     ){
#
#                     }
#
#
# """