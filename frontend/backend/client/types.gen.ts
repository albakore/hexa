// This file is auto-generated by @hey-api/openapi-ts

/**
 * AuthLoginRequest
 */
export type AuthLoginRequest = {
  /**
   * Nickname
   * nickname or email
   */
  nickname: string;
  /**
   * Password
   */
  password: string;
};

/**
 * AuthPasswordResetRequest
 */
export type AuthPasswordResetRequest = {
  /**
   * Id
   * User ID
   */
  id: string;
  /**
   * Initial Password
   * Initial password
   */
  initial_password: string;
  /**
   * New Password
   * New password account
   */
  new_password: string;
};

/**
 * AuthRegisterRequest
 */
export type AuthRegisterRequest = {
  /**
   * Email
   * Email
   */
  email: string;
  /**
   * Nickname
   * Nickname
   */
  nickname?: string | null;
  /**
   * Name
   * Name
   */
  name?: string | null;
  /**
   * Lastname
   * Lastname
   */
  lastname?: string | null;
  /**
   * Job Position
   * Job Position
   */
  job_position?: string | null;
  /**
   * Phone Number
   * Phone Number
   */
  phone_number?: string | null;
};

/**
 * CreateGroupRequest
 */
export type CreateGroupRequest = {
  /**
   * Name
   * Name of group
   */
  name: string;
  /**
   * Description
   * Description of group
   */
  description?: string | null;
};

/**
 * CreatePermissionRequest
 */
export type CreatePermissionRequest = {
  /**
   * Name
   * Name of permission
   */
  name: string;
  /**
   * Token
   * Unique token of permission
   */
  token: string;
  /**
   * Description
   * Description of permission
   */
  description?: string | null;
};

/**
 * CreateRoleRequest
 */
export type CreateRoleRequest = {
  /**
   * Name
   * Name of role
   */
  name: string;
  /**
   * Description
   * Description of role
   */
  description?: string | null;
};

/**
 * CreateUserRequest
 */
export type CreateUserRequest = {
  /**
   * Name
   */
  name?: string;
  /**
   * Lastname
   */
  lastname?: string;
  /**
   * Email
   */
  email?: string;
};

/**
 * GroupAddPermissionResponse
 */
export type GroupAddPermissionResponse = {
  /**
   * Id
   */
  id?: number | null;
  /**
   * Name
   */
  name: string;
  /**
   * Permissions
   */
  permissions?: Array<Permission> | null;
};

/**
 * GroupPermission
 */
export type GroupPermission = {
  /**
   * Id
   */
  id?: number | null;
  /**
   * Name
   */
  name: string;
  /**
   * Description
   */
  description?: string | null;
};

/**
 * GroupResponse
 */
export type GroupResponse = {
  /**
   * Id
   */
  id?: number | null;
  /**
   * Name
   */
  name?: string | null;
  /**
   * Description
   */
  description?: string | null;
  /**
   * Permissions
   */
  permissions?: Array<Permission> | null;
};

/**
 * HTTPValidationError
 */
export type HttpValidationError = {
  /**
   * Detail
   */
  detail?: Array<ValidationError>;
};

/**
 * Module
 */
export type Module = {
  /**
   * Id
   */
  id?: number | null;
  /**
   * Name
   */
  name: string;
  /**
   * Token
   */
  token: string;
  /**
   * Description
   */
  description?: string | null;
};

/**
 * Permission
 */
export type Permission = {
  /**
   * Id
   */
  id?: number | null;
  /**
   * Group Name
   */
  group_name?: string | null;
  /**
   * Name
   */
  name: string;
  /**
   * Token
   */
  token: string;
  /**
   * Description
   */
  description?: string | null;
};

/**
 * RefreshTokenRequest
 */
export type RefreshTokenRequest = {
  /**
   * Refresh Token
   * Refresh token
   */
  refresh_token: string;
};

/**
 * RefreshTokenResponse
 */
export type RefreshTokenResponse = {
  user: UserLoginResponseDto;
  /**
   * Permissions
   */
  permissions: Array<string>;
  /**
   * Token
   * Token
   */
  token: string;
  /**
   * Refresh Token
   * Refresh token
   */
  refresh_token: string;
};

/**
 * RoleAddGroupsResponse
 */
export type RoleAddGroupsResponse = {
  /**
   * Id
   */
  id?: number | null;
  /**
   * Name
   */
  name: string;
  /**
   * Groups
   */
  groups?: Array<GroupPermission> | null;
};

/**
 * RoleAddModulesResponse
 */
export type RoleAddModulesResponse = {
  /**
   * Id
   */
  id?: number | null;
  /**
   * Name
   */
  name: string;
  /**
   * Modules
   */
  modules?: Array<Module> | null;
};

/**
 * RoleAddPermissionResponse
 */
export type RoleAddPermissionResponse = {
  /**
   * Id
   */
  id?: number | null;
  /**
   * Name
   */
  name: string;
  /**
   * Permissions
   */
  permissions?: Array<Permission> | null;
};

/**
 * RoleRequest
 */
export type RoleRequest = {
  /**
   * Id
   */
  id: number;
  /**
   * Name
   */
  name: string;
};

/**
 * RoleResponse
 */
export type RoleResponse = {
  /**
   * Id
   */
  id?: number | null;
  /**
   * Name
   */
  name?: string | null;
  /**
   * Description
   */
  description?: string | null;
  /**
   * Groups
   */
  groups?: Array<GroupPermission> | null;
  /**
   * Permissions
   */
  permissions?: Array<Permission> | null;
  /**
   * Modules
   */
  modules?: Array<Module> | null;
};

/**
 * UserLoginResponseDTO
 */
export type UserLoginResponseDto = {
  /**
   * Id
   */
  id: string;
  /**
   * Nickname
   */
  nickname?: string | null;
  /**
   * Email
   */
  email?: string | null;
  /**
   * Name
   */
  name?: string | null;
  /**
   * Lastname
   */
  lastname?: string | null;
  /**
   * Job Position
   */
  job_position?: string | null;
  /**
   * Fk Role
   */
  fk_role?: number | null;
};

/**
 * ValidationError
 */
export type ValidationError = {
  /**
   * Location
   */
  loc: Array<string | number>;
  /**
   * Message
   */
  msg: string;
  /**
   * Error Type
   */
  type: string;
};

/**
 * VerifyTokenRequest
 */
export type VerifyTokenRequest = {
  /**
   * Token
   * Token
   */
  token: string;
};

export type RefreshTokenData = {
  body: RefreshTokenRequest;
  path?: never;
  query?: never;
  url: "/auth/v1/auth/refresh";
};

export type RefreshTokenErrors = {
  /**
   * Validation Error
   */
  422: HttpValidationError;
};

export type RefreshTokenError = RefreshTokenErrors[keyof RefreshTokenErrors];

export type RefreshTokenResponses = {
  /**
   * Successful Response
   */
  200: RefreshTokenResponse;
};

export type RefreshTokenResponse2 =
  RefreshTokenResponses[keyof RefreshTokenResponses];

export type VerifyTokenData = {
  body: VerifyTokenRequest;
  path?: never;
  query?: never;
  url: "/auth/v1/auth/verify";
};

export type VerifyTokenErrors = {
  /**
   * Validation Error
   */
  422: HttpValidationError;
};

export type VerifyTokenError = VerifyTokenErrors[keyof VerifyTokenErrors];

export type VerifyTokenResponses = {
  /**
   * Successful Response
   */
  200: unknown;
};

export type LoginData = {
  body: AuthLoginRequest;
  path?: never;
  query?: never;
  url: "/auth/v1/auth/login";
};

export type LoginErrors = {
  /**
   * Validation Error
   */
  422: HttpValidationError;
};

export type LoginError = LoginErrors[keyof LoginErrors];

export type LoginResponses = {
  /**
   * Successful Response
   */
  200: unknown;
};

export type RegisterData = {
  body: AuthRegisterRequest;
  path?: never;
  query?: never;
  url: "/auth/v1/auth/register";
};

export type RegisterErrors = {
  /**
   * Validation Error
   */
  422: HttpValidationError;
};

export type RegisterError = RegisterErrors[keyof RegisterErrors];

export type RegisterResponses = {
  /**
   * Successful Response
   */
  200: unknown;
};

export type PasswordResetData = {
  body: AuthPasswordResetRequest;
  path?: never;
  query?: never;
  url: "/auth/v1/auth/password_reset";
};

export type PasswordResetErrors = {
  /**
   * Validation Error
   */
  422: HttpValidationError;
};

export type PasswordResetError = PasswordResetErrors[keyof PasswordResetErrors];

export type PasswordResetResponses = {
  /**
   * Successful Response
   */
  200: unknown;
};

export type GetAllRolesData = {
  body?: never;
  path?: never;
  query?: never;
  url: "/rbac/v1/rbac/role";
};

export type GetAllRolesResponses = {
  /**
   * Successful Response
   */
  200: unknown;
};

export type CreateRoleData = {
  body: CreateRoleRequest;
  path?: never;
  query?: never;
  url: "/rbac/v1/rbac/role";
};

export type CreateRoleErrors = {
  /**
   * Validation Error
   */
  422: HttpValidationError;
};

export type CreateRoleError = CreateRoleErrors[keyof CreateRoleErrors];

export type CreateRoleResponses = {
  /**
   * Successful Response
   */
  200: unknown;
};

export type EditRoleData = {
  body?: never;
  path?: never;
  query?: never;
  url: "/rbac/v1/rbac/role";
};

export type EditRoleResponses = {
  /**
   * Successful Response
   */
  200: unknown;
};

export type DeleteRoleData = {
  body?: never;
  path: {
    /**
     * Id Role
     */
    id_role: number;
  };
  query?: never;
  url: "/rbac/v1/rbac/role/{id_role}";
};

export type DeleteRoleErrors = {
  /**
   * Validation Error
   */
  422: HttpValidationError;
};

export type DeleteRoleError = DeleteRoleErrors[keyof DeleteRoleErrors];

export type DeleteRoleResponses = {
  /**
   * Successful Response
   */
  200: unknown;
};

export type GetRoleData = {
  body?: never;
  path: {
    /**
     * Id Role
     */
    id_role: number;
  };
  query?: never;
  url: "/rbac/v1/rbac/role/{id_role}";
};

export type GetRoleErrors = {
  /**
   * Validation Error
   */
  422: HttpValidationError;
};

export type GetRoleError = GetRoleErrors[keyof GetRoleErrors];

export type GetRoleResponses = {
  /**
   * Successful Response
   */
  200: RoleResponse;
};

export type GetRoleResponse = GetRoleResponses[keyof GetRoleResponses];

export type GetAllRolePermissionsData = {
  body?: never;
  path: {
    /**
     * Id Role
     */
    id_role: number;
  };
  query?: never;
  url: "/rbac/v1/rbac/role/{id_role}/permission";
};

export type GetAllRolePermissionsErrors = {
  /**
   * Validation Error
   */
  422: HttpValidationError;
};

export type GetAllRolePermissionsError =
  GetAllRolePermissionsErrors[keyof GetAllRolePermissionsErrors];

export type GetAllRolePermissionsResponses = {
  /**
   * Response Rbac-Get All Role Permissions
   * Successful Response
   */
  200: Array<Permission>;
};

export type GetAllRolePermissionsResponse =
  GetAllRolePermissionsResponses[keyof GetAllRolePermissionsResponses];

export type AddPermissionsToRoleData = {
  /**
   * Permissions
   */
  body: Array<Permission>;
  path: {
    /**
     * Id Role
     */
    id_role: number;
  };
  query?: never;
  url: "/rbac/v1/rbac/role/{id_role}/add/permission";
};

export type AddPermissionsToRoleErrors = {
  /**
   * Validation Error
   */
  422: HttpValidationError;
};

export type AddPermissionsToRoleError =
  AddPermissionsToRoleErrors[keyof AddPermissionsToRoleErrors];

export type AddPermissionsToRoleResponses = {
  /**
   * Successful Response
   */
  200: RoleAddPermissionResponse;
};

export type AddPermissionsToRoleResponse =
  AddPermissionsToRoleResponses[keyof AddPermissionsToRoleResponses];

export type AddGroupsToRoleData = {
  /**
   * Groups
   */
  body: Array<GroupPermission>;
  path: {
    /**
     * Id Role
     */
    id_role: number;
  };
  query?: never;
  url: "/rbac/v1/rbac/role/{id_role}/add/groups";
};

export type AddGroupsToRoleErrors = {
  /**
   * Validation Error
   */
  422: HttpValidationError;
};

export type AddGroupsToRoleError =
  AddGroupsToRoleErrors[keyof AddGroupsToRoleErrors];

export type AddGroupsToRoleResponses = {
  /**
   * Successful Response
   */
  200: RoleAddGroupsResponse;
};

export type AddGroupsToRoleResponse =
  AddGroupsToRoleResponses[keyof AddGroupsToRoleResponses];

export type AddModulesToRoleData = {
  /**
   * Modules
   */
  body: Array<Module>;
  path: {
    /**
     * Id Role
     */
    id_role: number;
  };
  query?: never;
  url: "/rbac/v1/rbac/role/{id_role}/add/modules";
};

export type AddModulesToRoleErrors = {
  /**
   * Validation Error
   */
  422: HttpValidationError;
};

export type AddModulesToRoleError =
  AddModulesToRoleErrors[keyof AddModulesToRoleErrors];

export type AddModulesToRoleResponses = {
  /**
   * Successful Response
   */
  200: RoleAddModulesResponse;
};

export type AddModulesToRoleResponse =
  AddModulesToRoleResponses[keyof AddModulesToRoleResponses];

export type GetAllPermissionsData = {
  body?: never;
  path?: never;
  query?: never;
  url: "/rbac/v1/rbac/permission";
};

export type GetAllPermissionsResponses = {
  /**
   * Successful Response
   */
  200: unknown;
};

export type CreatePermissionData = {
  body: CreatePermissionRequest;
  path?: never;
  query?: never;
  url: "/rbac/v1/rbac/permission";
};

export type CreatePermissionErrors = {
  /**
   * Validation Error
   */
  422: HttpValidationError;
};

export type CreatePermissionError =
  CreatePermissionErrors[keyof CreatePermissionErrors];

export type CreatePermissionResponses = {
  /**
   * Successful Response
   */
  200: unknown;
};

export type EditPermissionData = {
  body?: never;
  path?: never;
  query: {
    /**
     * Permission
     */
    permission: unknown;
  };
  url: "/rbac/v1/rbac/permission";
};

export type EditPermissionErrors = {
  /**
   * Validation Error
   */
  422: HttpValidationError;
};

export type EditPermissionError =
  EditPermissionErrors[keyof EditPermissionErrors];

export type EditPermissionResponses = {
  /**
   * Successful Response
   */
  200: unknown;
};

export type DeletePermissionData = {
  body?: never;
  path: {
    /**
     * Id Permission
     */
    id_permission: number;
  };
  query?: never;
  url: "/rbac/v1/rbac/permission/{id_permission}";
};

export type DeletePermissionErrors = {
  /**
   * Validation Error
   */
  422: HttpValidationError;
};

export type DeletePermissionError =
  DeletePermissionErrors[keyof DeletePermissionErrors];

export type DeletePermissionResponses = {
  /**
   * Successful Response
   */
  200: unknown;
};

export type GetPermissionData = {
  body?: never;
  path: {
    /**
     * Id Permission
     */
    id_permission: number;
  };
  query?: never;
  url: "/rbac/v1/rbac/permission/{id_permission}";
};

export type GetPermissionErrors = {
  /**
   * Validation Error
   */
  422: HttpValidationError;
};

export type GetPermissionError = GetPermissionErrors[keyof GetPermissionErrors];

export type GetPermissionResponses = {
  /**
   * Successful Response
   */
  200: unknown;
};

export type GetAllGroupsData = {
  body?: never;
  path?: never;
  query?: never;
  url: "/rbac/v1/rbac/group";
};

export type GetAllGroupsResponses = {
  /**
   * Successful Response
   */
  200: unknown;
};

export type CreateGroupData = {
  body: CreateGroupRequest;
  path?: never;
  query?: never;
  url: "/rbac/v1/rbac/group";
};

export type CreateGroupErrors = {
  /**
   * Validation Error
   */
  422: HttpValidationError;
};

export type CreateGroupError = CreateGroupErrors[keyof CreateGroupErrors];

export type CreateGroupResponses = {
  /**
   * Successful Response
   */
  200: unknown;
};

export type GetGroupData = {
  body?: never;
  path: {
    /**
     * Id Group
     */
    id_group: number;
  };
  query?: never;
  url: "/rbac/v1/rbac/group/{id_group}";
};

export type GetGroupErrors = {
  /**
   * Validation Error
   */
  422: HttpValidationError;
};

export type GetGroupError = GetGroupErrors[keyof GetGroupErrors];

export type GetGroupResponses = {
  /**
   * Successful Response
   */
  200: GroupResponse;
};

export type GetGroupResponse = GetGroupResponses[keyof GetGroupResponses];

export type AddPermissionsToGroupData = {
  /**
   * Permissions
   */
  body: Array<Permission>;
  path: {
    /**
     * Id Group
     */
    id_group: number;
  };
  query?: never;
  url: "/rbac/v1/rbac/group/{id_group}/add/permission";
};

export type AddPermissionsToGroupErrors = {
  /**
   * Validation Error
   */
  422: HttpValidationError;
};

export type AddPermissionsToGroupError =
  AddPermissionsToGroupErrors[keyof AddPermissionsToGroupErrors];

export type AddPermissionsToGroupResponses = {
  /**
   * Successful Response
   */
  200: GroupAddPermissionResponse;
};

export type AddPermissionsToGroupResponse =
  AddPermissionsToGroupResponses[keyof AddPermissionsToGroupResponses];

export type GetUserListData = {
  body?: never;
  path?: never;
  query?: {
    /**
     * Limit
     */
    limit?: number;
    /**
     * Page
     */
    page?: number;
  };
  url: "/users/v1/users";
};

export type GetUserListErrors = {
  /**
   * Validation Error
   */
  422: HttpValidationError;
};

export type GetUserListError = GetUserListErrors[keyof GetUserListErrors];

export type GetUserListResponses = {
  /**
   * Successful Response
   */
  200: unknown;
};

export type CreateUserData = {
  body: CreateUserRequest;
  path?: never;
  query?: never;
  url: "/users/v1/users";
};

export type CreateUserErrors = {
  /**
   * Validation Error
   */
  422: HttpValidationError;
};

export type CreateUserError = CreateUserErrors[keyof CreateUserErrors];

export type CreateUserResponses = {
  /**
   * Successful Response
   */
  200: unknown;
};

export type GetUserData = {
  body?: never;
  path?: never;
  query: {
    /**
     * User Uuid
     */
    user_uuid: string;
  };
  url: "/users/v1/users/{user_id}";
};

export type GetUserErrors = {
  /**
   * Validation Error
   */
  422: HttpValidationError;
};

export type GetUserError = GetUserErrors[keyof GetUserErrors];

export type GetUserResponses = {
  /**
   * Successful Response
   */
  200: unknown;
};

export type AsignRoleData = {
  body: RoleRequest;
  path: {
    /**
     * User Uuid
     */
    user_uuid: string;
  };
  query?: never;
  url: "/users/v1/users/{user_uuid}/role";
};

export type AsignRoleErrors = {
  /**
   * Validation Error
   */
  422: HttpValidationError;
};

export type AsignRoleError = AsignRoleErrors[keyof AsignRoleErrors];

export type AsignRoleResponses = {
  /**
   * Successful Response
   */
  200: unknown;
};

export type GetAllProvidersData = {
  body?: never;
  path?: never;
  query?: {
    /**
     * Limit
     */
    limit?: number;
    /**
     * Page
     */
    page?: number;
  };
  url: "/providers/v1/providers";
};

export type GetAllProvidersErrors = {
  /**
   * Validation Error
   */
  422: HttpValidationError;
};

export type GetAllProvidersError =
  GetAllProvidersErrors[keyof GetAllProvidersErrors];

export type GetAllProvidersResponses = {
  /**
   * Successful Response
   */
  200: unknown;
};

export type GetBackendSchemaData = {
  body?: never;
  path?: never;
  query?: never;
  url: "/system/openapi_schema";
};

export type GetBackendSchemaResponses = {
  /**
   * Successful Response
   */
  200: unknown;
};

export type GetSystemPermissionsData = {
  body?: never;
  path?: never;
  query?: never;
  url: "/permissions";
};

export type GetSystemPermissionsResponses = {
  /**
   * Successful Response
   */
  200: unknown;
};

export type GetSystemModulesData = {
  body?: never;
  path?: never;
  query?: never;
  url: "/modules";
};

export type GetSystemModulesResponses = {
  /**
   * Successful Response
   */
  200: unknown;
};

export type ClientOptions = {
  baseUrl: "http://localhost:8000" | (string & {});
};
