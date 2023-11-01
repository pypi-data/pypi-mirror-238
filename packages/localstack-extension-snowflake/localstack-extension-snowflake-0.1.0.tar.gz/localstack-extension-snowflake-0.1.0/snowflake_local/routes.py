_E='precision'
_D='success'
_C='name'
_B='POST'
_A=True
import base64,gzip,json,logging,os.path,re,pyarrow,pyarrow.json
from localstack.aws.connect import connect_to
from localstack.http import Request,Response,route
from localstack.utils.aws.resources import get_or_create_bucket
from localstack.utils.strings import to_str
from localstack_ext.services.rds.engine_postgres import get_type_name
from snowflake_local.config import ASSETS_BUCKET_NAME,ASSETS_KEY_PREFIX
from snowflake_local.constants import PATH_QUERIES,PATH_SESSION
from snowflake_local.models import QueryResponse
from snowflake_local.queries import execute_query
from snowflake_local.storage import FileRef,StageType
LOG=logging.getLogger(__name__)
REGEX_FILE_FORMAT='\\s*(CREATE|DROP)\\s+.*FILE\\s+FORMAT\\s+(?:IF\\s+NOT\\s+EXISTS\\s+)?(.+)(\\s+TYPE\\s+=(.+))?'
class RequestHandler:
	@route(PATH_SESSION,methods=[_B])
	def session_request(self,request,**B):
		if request.args.get('delete')=='true':LOG.info('Deleting session data...')
		A={_D:_A};return Response.for_json(A,status=200)
	@route(f"{PATH_SESSION}/v1/login-request",methods=[_B])
	def session_login(self,request,**B):A={'data':{'nextAction':None,'token':'token123','masterToken':'masterToken123'},_D:_A};return Response.for_json(A,status=200)
	@route(f"{PATH_QUERIES}/query-request",methods=[_B])
	def start_query(self,request,**D):B=_get_data(request);C=B.get('sqlText','');A=handle_query_request(C);A=A.to_dict();return Response.for_json(A,status=200)
	@route(f"{PATH_QUERIES}/abort-request",methods=[_B])
	def abort_query(self,request,**A):return{_D:_A}
def handle_query_request(query):
	B=query;A=QueryResponse();A.data.parameters.append({_C:'TIMEZONE','value':'UTC'});B=B.strip(' ;');H=re.match('^\\s*PUT\\s+.+',B,flags=re.IGNORECASE)
	if H:return handle_put_file_query(B,A)
	I=re.match('^\\s*CREATE\\s+WAREHOUSE\\s.+',B,flags=re.IGNORECASE)
	if I:return A
	J=re.match('^\\s*USE\\s.+',B,flags=re.IGNORECASE)
	if J:return A
	K=re.match('^\\s*CREATE\\s+STORAGE\\s.+',B,flags=re.IGNORECASE)
	if K:return A
	L=re.match('^\\s*COPY\\s+INTO\\s.+',B,flags=re.IGNORECASE)
	if L:return A
	M=re.match(REGEX_FILE_FORMAT,B,flags=re.IGNORECASE)
	if M:return A
	C=execute_query(B)
	if C and C._context.columns:
		D=[];N=C._context.columns
		for O in C:D.append(list(O))
		F=[]
		for E in N:F.append({_C:E[_C],'type':get_type_name(E['type_oid']),'length':E['type_size'],_E:0,'scale':0,'nullable':_A})
		A.data.rowset=D;A.data.rowtype=F;A.data.total=len(D)
	G=re.match('.+FROM\\s+@',B);A.data.queryResultFormat='arrow'if G else'json'
	if G:A.data.rowsetBase64=_to_pyarrow_table_bytes_b64(A);A.data.rowset=[];A.data.rowtype=[]
	return A
def _to_pyarrow_table_bytes_b64(result):
	I='16777216';B=result;J={'byteLength':I,'charLength':I,'logicalType':'VARIANT',_E:'38','scale':'0','finalType':'T'};D=[];E=[A[_C].replace('_col','$')for A in B.data.rowtype]
	for K in range(len(E)):L=[A[K]for A in B.data.rowset];D.append(pyarrow.array(L))
	F=pyarrow.record_batch(D,names=E);G=pyarrow.BufferOutputStream();A=F.schema
	for C in range(len(A)):H=A.field(C);M=H.with_metadata(J);A=A.set(C,M);H=A.field(C)
	with pyarrow.ipc.new_stream(G,A)as N:N.write_batch(F)
	B=base64.b64encode(G.getvalue());return to_str(B)
def handle_put_file_query(query,result):
	I='test';A=result;D=re.match('^PUT\\s+(\\S+)\\s+(\\S+)',query);B=D.group(1);C=D.group(2);B=B.removeprefix('file://')
	if'/'not in C:C=f"{C}/{os.path.basename(B)}"
	E=FileRef.parse(C);F=E.get_path().lstrip('/');A.data.command='UPLOAD';A.data.src_locations=[B];get_or_create_bucket(ASSETS_BUCKET_NAME,s3_client=connect_to().s3);G=f"{ASSETS_BUCKET_NAME}/{ASSETS_KEY_PREFIX}"
	if E.stage.stage_type==StageType.USER:H=f"{G}{F}"
	else:H=f"{G}{os.path.dirname(F)}"
	A.data.stageInfo={'locationType':'S3','region':'us-east-1','endPoint':'s3.localhost.localstack.cloud:4566','location':H,'creds':{'AWS_KEY_ID':I,'AWS_SECRET_KEY':I}};A.data.sourceCompression='none';return A
def _get_data(request):
	A=request.data
	if isinstance(A,bytes):A=gzip.decompress(A);A=json.loads(to_str(A))
	return A