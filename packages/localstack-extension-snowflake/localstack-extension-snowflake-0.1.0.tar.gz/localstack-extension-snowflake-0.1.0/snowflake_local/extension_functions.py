import json
from localstack.utils.strings import to_str
def load_data(file_ref,file_format):
	from snowflake_local.storage import FILE_STORAGE as D,FileRef as E;F=E.parse(file_ref);A=D.load_file(F);A=json.loads(to_str(A));G=A if isinstance(A,list)else[A];B=[]
	for C in G:
		if isinstance(C,dict):B.append({'_col1':json.dumps(C)})
		else:B.append(C)
	return B