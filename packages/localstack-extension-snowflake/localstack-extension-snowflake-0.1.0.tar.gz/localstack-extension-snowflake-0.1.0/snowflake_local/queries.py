_A='test'
import base64,logging,re,time
from localstack.utils.net import get_free_tcp_port,wait_for_port_open
from localstack.utils.strings import to_bytes,to_str
from localstack_ext.utils.postgresql import Postgresql
from simple_ddl_parser import DDLParser
LOG=logging.getLogger(__name__)
class State:server=None
def execute_query(query,*C):
	A=query;D=start_postgres();A=fix_query(A);LOG.debug('Running query: %s',A)
	try:return D.run_query(A,*C)
	except Exception as B:
		if'already exists'in str(B):
			if'database'in str(B):return
			if'relation'in str(B):E=re.match('.*relation \\"(.+)\\" already exists',str(B)).group(1);D.run_query(f"DROP TABLE {E}",*C);return D.run_query(A,*C)
		raise
def fix_query(query):
	A=query;A=A.replace('\n',' ')
	def B(search,replace):return re.sub(search,replace,A,flags=re.IGNORECASE)
	if _is_create_table_query(A):A=B('(.+\\s)string(\\s*[,)].*)','\\1text\\2')
	A=B('^\\s*CREATE\\s+DATABASE\\s+IF\\s+NOT\\s+EXISTS','CREATE DATABASE');A=B('^\\s*CREATE\\s+OR\\s+REPLACE\\s+TABLE','CREATE TABLE');A=B('::\\s*VARIANT','');A=_create_tmp_table_for_file_queries(A);return A
def define_util_functions(server):A=server;A.run_query('CREATE EXTENSION IF NOT EXISTS plpython3u');B='\n    CREATE OR REPLACE FUNCTION parse_json (\n       content text\n    ) RETURNS text\n    LANGUAGE plpython3u IMMUTABLE\n    AS $$\n        return content\n    $$;\n    ';A.run_query(B);B='\n    CREATE OR REPLACE FUNCTION load_data (\n       file_ref text,\n       file_format text\n    ) RETURNS SETOF RECORD\n    LANGUAGE plpython3u IMMUTABLE\n    AS $$\n        from snowflake_local.extension_functions import load_data\n        return load_data(file_ref, file_format)\n    $$;\n    ';A.run_query(B)
def _is_create_table_query(query):
	A=DDLParser(query).run()
	if not A:return False
	return bool(A[0].get('table_name')and not A[0].get('alter'))
def _create_tmp_table_for_file_queries(query):
	A=query;C='(\\s*SELECT\\s+.+\\sFROM\\s+)(@[^\\(\\s]+)(\\s*\\([^\\)]+\\))?';F=re.match(C,A)
	if not F:return A
	G=re.findall('\\$\\d+',A);D='_col1 TEXT';B=[int(A.removeprefix('$'))for A in G]
	if B:H=list(range(1,max(B)+1));D=','.join([f"_col{A} TEXT"for A in H])
	def I(match):A=match;B=to_str(base64.b64encode(to_bytes(A.group(3)or'')));return f"{A.group(1)} load_data('{A.group(2)}', '{B}') as _tmp({D})"
	A=re.sub(C,I,A)
	if B:
		for E in range(max(B),0,-1):A=A.replace(f"${E}",f"_col{E}")
	return A
def start_postgres(user=_A,password=_A,database=_A):
	if not State.server:
		A=get_free_tcp_port();State.server=Postgresql(port=A,user=user,password=password,database=database,boot_timeout=30,include_python_venv_libs=True);time.sleep(1)
		try:B=20;wait_for_port_open(A,retries=B,sleep_time=.8)
		except Exception:raise Exception('Unable to start up Postgres process (health check failed after 10 secs)')
		define_util_functions(State.server)
	return State.server