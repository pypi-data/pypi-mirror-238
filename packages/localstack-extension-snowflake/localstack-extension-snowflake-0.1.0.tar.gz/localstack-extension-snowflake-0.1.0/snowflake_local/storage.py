import dataclasses,gzip,os.path,re
from abc import ABC,abstractmethod
from enum import Enum
from localstack.aws.connect import connect_to
from snowflake_local.config import ASSETS_BUCKET_NAME,ASSETS_KEY_PREFIX
REGEX_FILE_REF='^(@[~%]?)([^/]+)?(/.+)?'
class StageType(Enum):
	USER='USER';TABLE='TABLE';NAMED='NAMED'
	@classmethod
	def get(B,identifier):
		A=identifier
		if A.startswith('@~'):return StageType.USER
		if A.startswith('@%'):return StageType.TABLE
		return StageType.NAMED
@dataclasses.dataclass
class Stage:
	stage_type:StageType;name:str
	def get_path(A):return os.path.join(A.stage_type.value,A.name)
	@classmethod
	def parse(E,identifier):
		A=identifier;D=re.match(REGEX_FILE_REF,A);B=StageType.get(A);C=D.group(2)
		if B==StageType.USER:C='test-user'
		return Stage(stage_type=B,name=C)
@dataclasses.dataclass
class FileRef:
	stage:Stage;path:str
	def get_path(A):return os.path.join(A.stage.get_path(),A.path.lstrip('/'))
	@classmethod
	def parse(D,identifier):A=identifier;B=re.match(REGEX_FILE_REF,A);C=Stage.parse(A);return FileRef(stage=C,path=B.group(3)or'')
class FileStorage(ABC):
	@abstractmethod
	def store_file(self,file,content):0
	@abstractmethod
	def load_file(self,file):0
class FileStorageS3(FileStorage):
	def store_file(A,file,content):B=A._client();C=A._get_s3_key(file);B.put_object(Bucket=ASSETS_BUCKET_NAME,Key=C,Body=content)
	def load_file(B,file):
		E='Body';C=B._client();D=B._get_s3_key(file)
		try:A=C.get_object(Bucket=ASSETS_BUCKET_NAME,Key=D);return A[E].read()
		except Exception as F:
			if'NoSuchKey'not in str(F):raise
			A=C.get_object(Bucket=ASSETS_BUCKET_NAME,Key=f"{D}.gz");G=A[E].read();return gzip.decompress(G)
	def _get_s3_key(A,file):return f"{ASSETS_KEY_PREFIX}{file.get_path().lstrip('/')}"
	def _client(A):return connect_to().s3
FILE_STORAGE=FileStorageS3()