from localstack.extensions.api import Extension
from localstack.extensions.api.http import RouteHandler,Router
from snowflake_local.routes import RequestHandler
class SnowflakeExtension(Extension):
	name='snowflake'
	def update_gateway_routes(A,router):router.add(RequestHandler())