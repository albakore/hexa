import json
import pprint
from modules.yiqi_erp.domain.entity.factura_compra import FacturaDeCompra

object =  json.load(open("modules/yiqi_erp/test/page_configuration.json", "r"))

for key_instance in object:
	class_str = [
		"from pydantic import Field, BaseModel\n\n",
		f"""class {object[key_instance]["name"]}:\n"""
	]
	attributes_str = []
	for key in FacturaDeCompra.get_attributes():

		for attribute in object[key_instance]['attributes']:
			if key == attribute["name"]:
				attributes_str.append(''.join((
					f"""\t{attribute["name"]}""",
					" = ",
					f"""Field(..., serialization_alias="{attribute["attId"]}")""",
				)))
				break

	class_str.append("\n".join(attributes_str))
	print(*class_str,file=open("modules/yiqi_erp/test/model.py","w+"))