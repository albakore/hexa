import json
import pprint
from typing import get_type_hints
from typing_extensions import get_annotations
import rich as r
from modules.yiqi_erp.domain.entity.factura_compra import FacturaDeCompra

object =  json.load(open("modules/yiqi_erp/test/page_configuration.json", "r"))

for key_instance in object:
	class_str = [
		"from pydantic import Field, BaseModel\n",
		"\nimport typing",
		"\nimport datetime",
		f"""\nclass {object[key_instance]["name"]}:\n\n"""
	]
	attributes_str = []
	for key in FacturaDeCompra.get_attributes():
		atributo_encontrado = None
		for attribute in object[key_instance]['attributes']:
			if key == attribute["name"]:
				atributo_encontrado = attribute["attId"]
				break
		
		attributes_str.append(''.join((
			f"""\t{key} : {get_type_hints(FacturaDeCompra).get(key)}""",
			"" if not atributo_encontrado else " = ",
			"" if not atributo_encontrado else f"""Field(..., serialization_alias="{attribute["attId"]}")""",
		)))
		
		if not atributo_encontrado:
			r.print(f"No se encuentra '{key}' en la clase")

	class_str.append("\n".join(attributes_str))
	print(*class_str,file=open("modules/yiqi_erp/test/model.py","w+"))