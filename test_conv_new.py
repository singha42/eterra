import json

out_json=list()
		
class dnp3_mapping():
	def __init__(self,map_file):
		self.c_ao = 0
		self.c_bo = 0
		self.c_ai = 0
		self.c_bi = 0
		with open(map_file, 'r') as f:
			self.file_dict = json.load(f) 
		
		self.out_json= list()
		
	def assign_val(self,data_type,group,variation,index,name,description,measurement_type,measurement_id):
		records = dict()
		records["data_type"] = data_type
		records["index"] = index
		records["group"] = group
		records["variation"] = variation
		records["description"] = descriptio
		records["name"] = name
		records["measurement_type"] = measurement_type
		records["measurement_id"] = measurement_id
			
		self.out_json.append(records)

	def dump_json(self,out_json,out_file):
		with open(out_file, 'w') as fp:
			out_dict= dict({'points':out_json})
			json.dump(out_dict,fp)

	def _create_cim_object_map(self):
		feeders = self.file_dict.get("feeders",[])
		for x in feeders:
			measurements = x.get("measurements",[])
			capacitors = x.get("capacitors",[])
			regulators = x.get("regulators",[])
			switches = x.get("switches",[])
			solarpanels = x.get("solarpanels",[])
				
		for m in measurements:
			measurement_type = m.get("measurementType")
			measurement_id = m.get("mRID")
			name =  m.get("name")
			description = "Equipment is " + m['name'] + "," + m['ConductingEquipment_type'] + " and phase is " + m['phases']
					
			if m['MeasurementClass'] == "Analog":
				self.assign_val("AO",42,3,self.c_ao,name,description,measurement_type,measurement_id)
				self.c_ao += 1
			elif m['MeasurementClass'] == "Discrete":
				self.assign_val("BO",11,1,self.c_bo,name,description,measurement_type,measurement_id)
				self.c_bo += 1
		
		for m in capacitors:
			measurement_id = m.get("mRID")
			name =  m.get("name")
			description = "Capacitor, " + m['name'] + "," + "phase -" + m['phases']
			if "targetDeadband" in m['capacitors']:
				self.assign_val("AI",32,3,self.c_ai,name,description,measurement_type,measurement_id)
				self.c_ai += 1
			else
				self.assign_val("BI",2,1,self.c_bi,name,description,None,measurement_id)
				self.c_bi +=1
		
		for m in switches:
			measurement_id = m.get("mRID")
			name = m.get("name")
			description = "Switch, " + m['name'] + "phases - " + m['phases']
			self.assign_val("BI",2,1,self.c_bi,name,description,None,measurement_id)
			self.c_bi +=1
			
		for m in regulators:
			measurement_id = m.get("mRID")
			name = m.get("bankName")
			for i in range(m['size']):
				description = "Regulator, " + m['tankName'][i] + "phases - " + m['endPhases'][i]
				self.assign_val("BI",2,1,self.c_bi,name,description,None,measurement_id)
				self.c_ai +=1
				

		return self.out_json

	test1 = dnp3_mapping('model_dict.json')
	a = test1._create_cim_object_map()
	test1.dump_json(a,'points.json')
	print(test1.out_json)