from . import permissions, search, satellite, metrics, policies, integration_log, integration_external_api, work_os, admin, integration_slack, integration_datahub, integration_github, audit, etl, integration_code_repository, integration_app, registry, cord, datastore, identities, inventory, encryption, integration_sso, native_user, integration_kms, sidecar, integration_cloud
import grpc

SERVER_URL = "adminv2.api.formalcloud.net:443"

class Client(object):
	"""Formal Admin API Client"""

	def __init__(self, api_key):
		"""Constructor.

		Args:
			api_key: Formal API Key
		"""
		self.PermissionClient = permissions.PermissionService(SERVER_URL, api_key)
		self.SearchClient = search.SearchService(SERVER_URL, api_key)
		self.SatelliteClient = satellite.SatelliteService(SERVER_URL, api_key)
		self.MetricsClient = metrics.MetricsService(SERVER_URL, api_key)
		self.PolicyClient = policies.PolicyService(SERVER_URL, api_key)
		self.LogsClient = integration_log.LogsService(SERVER_URL, api_key)
		self.ExternalApiClient = integration_external_api.ExternalApiService(SERVER_URL, api_key)
		self.DSyncClient = work_os.DSyncService(SERVER_URL, api_key)
		self.DevClient = admin.DevService(SERVER_URL, api_key)
		self.SlackClient = integration_slack.SlackService(SERVER_URL, api_key)
		self.DatahubClient = integration_datahub.DatahubService(SERVER_URL, api_key)
		self.GithubClient = integration_github.GithubService(SERVER_URL, api_key)
		self.AuditLogsClient = audit.AuditLogsService(SERVER_URL, api_key)
		self.ETLClient = etl.ETLService(SERVER_URL, api_key)
		self.CodeRepositoryClient = integration_code_repository.CodeRepositoryService(SERVER_URL, api_key)
		self.AppClient = integration_app.AppService(SERVER_URL, api_key)
		self.RegistryClient = registry.RegistryService(SERVER_URL, api_key)
		self.CordClient = cord.CordService(SERVER_URL, api_key)
		self.DataStoreClient = datastore.DataStoreService(SERVER_URL, api_key)
		self.UserClient = identities.UserService(SERVER_URL, api_key)
		self.GroupClient = identities.GroupService(SERVER_URL, api_key)
		self.InventoryClient = inventory.InventoryService(SERVER_URL, api_key)
		self.FieldEncryptionPolicyClient = encryption.FieldEncryptionPolicyService(SERVER_URL, api_key)
		self.FieldEncryptionClient = encryption.FieldEncryptionService(SERVER_URL, api_key)
		self.SsoClient = integration_sso.SsoService(SERVER_URL, api_key)
		self.NativeUserClient = native_user.NativeUserService(SERVER_URL, api_key)
		self.KmsClient = integration_kms.KmsService(SERVER_URL, api_key)
		self.SidecarClient = sidecar.SidecarService(SERVER_URL, api_key)
		self.CloudClient = integration_cloud.CloudService(SERVER_URL, api_key)
