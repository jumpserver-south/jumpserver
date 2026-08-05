# JumpServer 数据库表结构说明文档

> **版本：** v4.10.17 LTS
> **数据库：** MySQL 10.6.18-MariaDB
> **表总数：** 180
> **生成时间：** 自动生成

---

## 目录

- [账户管理（Accounts）](#accounts)（24 张表）
- [访问控制（ACLs）](#acls)（12 张表）
- [资产管理（Assets）](#assets)（27 张表）
- [审计日志（Audits）](#audits)（7 张表）
- [Django 认证（Auth）](#auth)（3 张表）
- [认证令牌（Authentication）](#authentication)（7 张表）
- [验证码（Captcha）](#captcha)（1 张表）
- [Django 框架（Django）](#django)（12 张表）
- [标签管理（Labels）](#labels)（2 张表）
- [通知消息（Notifications）](#notifications)（7 张表）
- [OAuth2（OAuth2 Provider）](#oauth2)（5 张表）
- [运维作业（Ops）](#ops)（10 张表）
- [组织管理（Organizations）](#orgs)（1 张表）
- [权限管理（Perms）](#perms)（6 张表）
- [RBAC 角色（RBAC）](#rbac)（4 张表）
- [报表（Reports）](#reports)（1 张表）
- [系统设置（Settings）](#settings)（2 张表）
- [终端会话（Terminal）](#terminal)（18 张表）
- [工单系统（Tickets）](#tickets)（14 张表）
- [用户管理（Users）](#users)（6 张表）
- [企业版功能（X-Pack）](#xpack)（10 张表）

---

## 通用字段说明

以下字段在大多数表中存在，后续各表不再重复说明：

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `id` | CHAR(32) | 主键，UUID 格式（无连字符） |
| `org_id` | VARCHAR(36) | 所属组织 ID，用于多租户数据隔离 |
| `created_by` | VARCHAR(128) | 创建者用户名 |
| `updated_by` | VARCHAR(128) | 最后更新者用户名 |
| `date_created` | DATETIME(6) | 记录创建时间 |
| `date_updated` | DATETIME(6) | 记录最后更新时间 |
| `comment` | LONGTEXT | 备注信息 |

---

## 账户管理（Accounts）

管理资产上的托管账户、凭据、自动化改密/推送/检测等

### `accounts_account`

**托管账户，存储资产上托管的用户名/密码/密钥等凭据信息**

| 字段 | 类型 | 可空 | 说明 |
| --- | --- | --- | --- |
| `created_by` | VARCHAR(128) | 是 | 创建者用户名 |
| `updated_by` | VARCHAR(128) | 是 | 最后更新者用户名 |
| `date_created` | DATETIME(6) | 是 | 创建时间 |
| `date_updated` | DATETIME(6) | 否 | 更新时间 |
| `comment` | LONGTEXT | 否 | 备注 |
| `id` | CHAR(32) | 否 | 主键，UUID 格式（无连字符，32 位） |
| `org_id` | VARCHAR(36) | 否 | 所属组织 ID，用于多租户数据隔离 |
| `connectivity` | VARCHAR(16) | 否 | 连通性状态 |
| `date_verified` | DATETIME(6) | 是 | 最后验证时间 |
| `_secret` | LONGTEXT | 是 | 加密存储的密钥/密码 |
| `name` | VARCHAR(128) | 否 | Username |
| `username` | VARCHAR(128) | 否 | Username |
| `secret_type` | VARCHAR(16) | 否 | Secret type |
| `privileged` | BOOLEAN | 否 | 是否特权账户 |
| `is_active` | BOOLEAN | 否 | Active |
| `version` | INT | 否 | Version |
| `source` | VARCHAR(30) | 否 | Source |
| `source_id` | VARCHAR(128) | 是 | Source ID |
| `asset_id` | CHAR(32) | 否 | 关联资产 ID |
| `su_from_id` | CHAR(32) | 是 | 提权来源账户 ID |
| `change_secret_status` | VARCHAR(16) | 是 | Change secret status |
| `date_change_secret` | DATETIME(6) | 是 | Date change secret |
| `date_last_login` | DATETIME(6) | 是 | Date last access |
| `login_by` | VARCHAR(128) | 是 | Access by |
| `secret_reset` | BOOLEAN | 否 | Secret reset |

**索引：**

- PRIMARY KEY: id
- UNIQUE `accounts_account_username_asset_id_secret_type_1892cc9f_uniq`: username,asset_id,secret_type
- UNIQUE `accounts_account_name_asset_id_d07d7988_uniq`: name,asset_id
- INDEX `accounts_account_username_asset_id_secret_type_1892cc9f_uniq`: username,asset_id,secret_type
- INDEX `accounts_account_name_asset_id_d07d7988_uniq`: name,asset_id
- INDEX `accounts_account_org_id_4b4ddfef`: org_id
- INDEX `accounts_account_username_b5f69a28`: username
- INDEX `accounts_account_asset_id_d77d9aa0_fk_assets_asset_id`: asset_id
- INDEX `accounts_account_su_from_id_1845461a_fk_accounts_account_id`: su_from_id
- FK `accounts_account_asset_id_d77d9aa0_fk_assets_asset_id`: asset_id → `assets_asset`.id
- FK `accounts_account_su_from_id_1845461a_fk_accounts_account_id`: su_from_id → `accounts_account`.id

---

### `accounts_accountrisk`

**账户风险记录，检测到的密码泄露、权限异常等风险事件**

| 字段 | 类型 | 可空 | 说明 |
| --- | --- | --- | --- |
| `created_by` | VARCHAR(128) | 是 | 创建者用户名 |
| `updated_by` | VARCHAR(128) | 是 | 最后更新者用户名 |
| `date_created` | DATETIME(6) | 是 | 创建时间 |
| `date_updated` | DATETIME(6) | 否 | 更新时间 |
| `comment` | LONGTEXT | 否 | 备注 |
| `id` | CHAR(32) | 否 | 主键，UUID 格式（无连字符，32 位） |
| `org_id` | VARCHAR(36) | 否 | 所属组织 ID，用于多租户数据隔离 |
| `username` | VARCHAR(128) | 否 | Username |
| `risk` | VARCHAR(128) | 否 | Risk |
| `status` | VARCHAR(32) | 否 | Status |
| `details` | LONGTEXT | 否 | Detail |
| `account_id` | CHAR(32) | 是 | account 的关联 ID |
| `asset_id` | CHAR(32) | 否 | 关联资产 ID |
| `gathered_account_id` | CHAR(32) | 是 | gathered_account 的关联 ID |

**索引：**

- PRIMARY KEY: id
- UNIQUE `accounts_accountrisk_asset_id_username_risk_5176986c_uniq`: asset_id,username,risk
- INDEX `accounts_accountrisk_asset_id_username_risk_5176986c_uniq`: asset_id,username,risk
- INDEX `accounts_accountrisk_account_id_f5acf22a_fk_accounts_account_id`: account_id
- INDEX `accounts_accountrisk_gathered_account_id_8aa18366_fk_accounts_`: gathered_account_id
- INDEX `accounts_accountrisk_org_id_6d4b24c9`: org_id
- FK `accounts_accountrisk_account_id_f5acf22a_fk_accounts_account_id`: account_id → `accounts_account`.id
- FK `accounts_accountrisk_asset_id_9599bb46_fk_assets_asset_id`: asset_id → `assets_asset`.id
- FK `accounts_accountrisk_gathered_account_id_8aa18366_fk_accounts_`: gathered_account_id → `accounts_gatheredaccount`.id

---

### `accounts_accounttemplate`

**账户模板，用于批量创建相同凭据的账户**

| 字段 | 类型 | 可空 | 说明 |
| --- | --- | --- | --- |
| `created_by` | VARCHAR(128) | 是 | 创建者用户名 |
| `updated_by` | VARCHAR(128) | 是 | 最后更新者用户名 |
| `date_created` | DATETIME(6) | 是 | 创建时间 |
| `date_updated` | DATETIME(6) | 否 | 更新时间 |
| `comment` | LONGTEXT | 否 | 备注 |
| `id` | CHAR(32) | 否 | 主键，UUID 格式（无连字符，32 位） |
| `org_id` | VARCHAR(36) | 否 | 所属组织 ID，用于多租户数据隔离 |
| `_secret` | LONGTEXT | 是 | 加密存储的密钥/密码 |
| `secret_strategy` | VARCHAR(16) | 否 | Secret strategy |
| `password_rules` | LONGTEXT | 否 | Password rules |
| `name` | VARCHAR(128) | 否 | Username |
| `username` | VARCHAR(128) | 否 | Username |
| `secret_type` | VARCHAR(16) | 否 | Secret type |
| `privileged` | BOOLEAN | 否 | 是否特权账户 |
| `is_active` | BOOLEAN | 否 | Active |
| `auto_push` | BOOLEAN | 否 | Auto push |
| `push_params` | LONGTEXT | 否 | Push params |
| `su_from_id` | CHAR(32) | 是 | 提权来源账户 ID |

**索引：**

- PRIMARY KEY: id
- UNIQUE `accounts_accounttemplate_name_org_id_d399e665_uniq`: name,org_id
- INDEX `accounts_accounttemplate_name_org_id_d399e665_uniq`: name,org_id
- INDEX `accounts_accounttemplate_org_id_92efd0a8`: org_id
- INDEX `accounts_accounttemplate_username_379784d9`: username
- INDEX `accounts_accounttemp_su_from_id_695954f2_fk_accounts_`: su_from_id
- FK `accounts_accounttemp_su_from_id_695954f2_fk_accounts_`: su_from_id → `accounts_accounttemplate`.id

---

### `accounts_accounttemplate_platforms`

**账户模板与平台的多对多关联**

| 字段 | 类型 | 可空 | 说明 |
| --- | --- | --- | --- |
| `id` | INT | 否 | 主键，UUID 格式（无连字符，32 位） |
| `accounttemplate_id` | CHAR(32) | 否 | accounttemplate 的关联 ID |
| `platform_id` | INT | 否 | platform 的关联 ID |

**索引：**

- PRIMARY KEY: id
- UNIQUE `accounts_accounttemplate_accounttemplate_id_platf_640c92a2_uniq`: accounttemplate_id,platform_id
- INDEX `accounts_accounttemplate_accounttemplate_id_platf_640c92a2_uniq`: accounttemplate_id,platform_id
- INDEX `accounts_accounttemp_platform_id_2bd7c470_fk_assets_pl`: platform_id
- FK `accounts_accounttemp_accounttemplate_id_c6c5dec6_fk_accounts_`: accounttemplate_id → `accounts_accounttemplate`.id
- FK `accounts_accounttemp_platform_id_2bd7c470_fk_assets_pl`: platform_id → `assets_platform`.id

---

### `accounts_backupaccountautomation`

**账户备份自动化任务配置**

| 字段 | 类型 | 可空 | 说明 |
| --- | --- | --- | --- |
| `baseautomation_ptr_id` | CHAR(32) | 否 | baseautomation_ptr 的关联 ID |
| `types` | LONGTEXT | 否 | Backup type |
| `backup_type` | VARCHAR(128) | 否 | Backup type |
| `is_password_divided_by_email` | BOOLEAN | 否 | Password divided |
| `is_password_divided_by_obj_storage` | BOOLEAN | 否 | Password divided |
| `zip_encrypt_password` | VARCHAR(8192) | 是 | - |

**索引：**

- PRIMARY KEY: baseautomation_ptr_id
- FK `accounts_backupaccou_baseautomation_ptr_i_9d415f6c_fk_assets_ba`: baseautomation_ptr_id → `assets_baseautomation`.id

---

### `accounts_backupaccountautomation_obj_recipients_part_one`

**账户备份通知接收人（组织）- 第一部分**

| 字段 | 类型 | 可空 | 说明 |
| --- | --- | --- | --- |
| `id` | INT | 否 | 主键，UUID 格式（无连字符，32 位） |
| `backupaccountautomation_id` | CHAR(32) | 否 | backupaccountautomation 的关联 ID |
| `replaystorage_id` | CHAR(32) | 否 | replaystorage 的关联 ID |

**索引：**

- PRIMARY KEY: id
- UNIQUE `accounts_backupaccountau_backupaccountautomation__49ede5e4_uniq`: backupaccountautomation_id,replaystorage_id
- INDEX `accounts_backupaccountau_backupaccountautomation__49ede5e4_uniq`: backupaccountautomation_id,replaystorage_id
- INDEX `accounts_backupaccou_replaystorage_id_5a387a66_fk_terminal_`: replaystorage_id
- FK `accounts_backupaccou_backupaccountautomat_c2386bc1_fk_accounts_`: backupaccountautomation_id → `accounts_backupaccountautomation`.baseautomation_ptr_id
- FK `accounts_backupaccou_replaystorage_id_5a387a66_fk_terminal_`: replaystorage_id → `terminal_replaystorage`.id

---

### `accounts_backupaccountautomation_obj_recipients_part_two`

**账户备份通知接收人（组织）- 第二部分**

| 字段 | 类型 | 可空 | 说明 |
| --- | --- | --- | --- |
| `id` | INT | 否 | 主键，UUID 格式（无连字符，32 位） |
| `backupaccountautomation_id` | CHAR(32) | 否 | backupaccountautomation 的关联 ID |
| `replaystorage_id` | CHAR(32) | 否 | replaystorage 的关联 ID |

**索引：**

- PRIMARY KEY: id
- UNIQUE `accounts_backupaccountau_backupaccountautomation__70add3bb_uniq`: backupaccountautomation_id,replaystorage_id
- INDEX `accounts_backupaccountau_backupaccountautomation__70add3bb_uniq`: backupaccountautomation_id,replaystorage_id
- INDEX `accounts_backupaccou_replaystorage_id_a713b2a8_fk_terminal_`: replaystorage_id
- FK `accounts_backupaccou_backupaccountautomat_ca899579_fk_accounts_`: backupaccountautomation_id → `accounts_backupaccountautomation`.baseautomation_ptr_id
- FK `accounts_backupaccou_replaystorage_id_a713b2a8_fk_terminal_`: replaystorage_id → `terminal_replaystorage`.id

---

### `accounts_backupaccountautomation_recipients_part_one`

**账户备份通知接收人 - 第一部分**

| 字段 | 类型 | 可空 | 说明 |
| --- | --- | --- | --- |
| `id` | INT | 否 | 主键，UUID 格式（无连字符，32 位） |
| `backupaccountautomation_id` | CHAR(32) | 否 | backupaccountautomation 的关联 ID |
| `user_id` | CHAR(32) | 否 | 用户 ID |

**索引：**

- PRIMARY KEY: id
- UNIQUE `accounts_backupaccountau_backupaccountautomation__5914fa53_uniq`: backupaccountautomation_id,user_id
- INDEX `accounts_backupaccountau_backupaccountautomation__5914fa53_uniq`: backupaccountautomation_id,user_id
- INDEX `accounts_backupaccou_user_id_861c387f_fk_users_use`: user_id
- FK `accounts_backupaccou_backupaccountautomat_4096eac3_fk_accounts_`: backupaccountautomation_id → `accounts_backupaccountautomation`.baseautomation_ptr_id
- FK `accounts_backupaccou_user_id_861c387f_fk_users_use`: user_id → `users_user`.id

---

### `accounts_backupaccountautomation_recipients_part_two`

**账户备份通知接收人 - 第二部分**

| 字段 | 类型 | 可空 | 说明 |
| --- | --- | --- | --- |
| `id` | INT | 否 | 主键，UUID 格式（无连字符，32 位） |
| `backupaccountautomation_id` | CHAR(32) | 否 | backupaccountautomation 的关联 ID |
| `user_id` | CHAR(32) | 否 | 用户 ID |

**索引：**

- PRIMARY KEY: id
- UNIQUE `accounts_backupaccountau_backupaccountautomation__9f2d7980_uniq`: backupaccountautomation_id,user_id
- INDEX `accounts_backupaccountau_backupaccountautomation__9f2d7980_uniq`: backupaccountautomation_id,user_id
- INDEX `accounts_backupaccou_user_id_652e90a7_fk_users_use`: user_id
- FK `accounts_backupaccou_backupaccountautomat_cb778f55_fk_accounts_`: backupaccountautomation_id → `accounts_backupaccountautomation`.baseautomation_ptr_id
- FK `accounts_backupaccou_user_id_652e90a7_fk_users_use`: user_id → `users_user`.id

---

### `accounts_changesecretautomation`

**自动改密自动化任务配置**

| 字段 | 类型 | 可空 | 说明 |
| --- | --- | --- | --- |
| `baseautomation_ptr_id` | CHAR(32) | 否 | baseautomation_ptr 的关联 ID |
| `secret_type` | VARCHAR(16) | 否 | Secret type |
| `secret` | LONGTEXT | 是 | 密钥/密码 |
| `secret_strategy` | VARCHAR(16) | 否 | Secret strategy |
| `password_rules` | LONGTEXT | 否 | Password rules |
| `ssh_key_change_strategy` | VARCHAR(16) | 否 | SSH key change strategy |
| `check_conn_after_change` | BOOLEAN | 否 | Check connection after change |

**索引：**

- PRIMARY KEY: baseautomation_ptr_id
- FK `accounts_changesecre_baseautomation_ptr_i_55ccffbc_fk_assets_ba`: baseautomation_ptr_id → `assets_baseautomation`.id

---

### `accounts_changesecretautomation_recipients`

**自动改密通知接收人**

| 字段 | 类型 | 可空 | 说明 |
| --- | --- | --- | --- |
| `id` | INT | 否 | 主键，UUID 格式（无连字符，32 位） |
| `changesecretautomation_id` | CHAR(32) | 否 | changesecretautomation 的关联 ID |
| `user_id` | CHAR(32) | 否 | 用户 ID |

**索引：**

- PRIMARY KEY: id
- UNIQUE `accounts_changesecretaut_changesecretautomation_i_e3af8d02_uniq`: changesecretautomation_id,user_id
- INDEX `accounts_changesecretaut_changesecretautomation_i_e3af8d02_uniq`: changesecretautomation_id,user_id
- INDEX `accounts_changesecre_user_id_9861c38f_fk_users_use`: user_id
- FK `accounts_changesecre_changesecretautomati_10753100_fk_accounts_`: changesecretautomation_id → `accounts_changesecretautomation`.baseautomation_ptr_id
- FK `accounts_changesecre_user_id_9861c38f_fk_users_use`: user_id → `users_user`.id

---

### `accounts_changesecretrecord`

**改密执行记录**

| 字段 | 类型 | 可空 | 说明 |
| --- | --- | --- | --- |
| `created_by` | VARCHAR(128) | 是 | 创建者用户名 |
| `updated_by` | VARCHAR(128) | 是 | 最后更新者用户名 |
| `date_created` | DATETIME(6) | 是 | 创建时间 |
| `date_updated` | DATETIME(6) | 否 | 更新时间 |
| `comment` | LONGTEXT | 否 | 备注 |
| `id` | CHAR(32) | 否 | 主键，UUID 格式（无连字符，32 位） |
| `old_secret` | LONGTEXT | 是 | - |
| `new_secret` | LONGTEXT | 是 | - |
| `date_finished` | DATETIME(6) | 是 | Date finished |
| `status` | VARCHAR(16) | 否 | Status |
| `error` | LONGTEXT | 是 | Error |
| `account_id` | CHAR(32) | 是 | account 的关联 ID |
| `asset_id` | CHAR(32) | 是 | 关联资产 ID |
| `execution_id` | CHAR(32) | 是 | 执行记录 ID |
| `ignore_fail` | BOOLEAN | 否 | Ignore fail |

**索引：**

- PRIMARY KEY: id
- INDEX `accounts_changesecre_account_id_e263b671_fk_accounts_`: account_id
- INDEX `accounts_changesecretrecord_asset_id_65430b74_fk_assets_asset_id`: asset_id
- INDEX `accounts_changesecre_execution_id_bbde8815_fk_assets_au`: execution_id
- INDEX `accounts_changesecretrecord_date_finished_9b0d34ae`: date_finished
- FK `accounts_changesecre_account_id_e263b671_fk_accounts_`: account_id → `accounts_account`.id
- FK `accounts_changesecre_execution_id_bbde8815_fk_assets_au`: execution_id → `assets_automationexecution`.id
- FK `accounts_changesecretrecord_asset_id_65430b74_fk_assets_asset_id`: asset_id → `assets_asset`.id

---

### `accounts_checkaccountautomation`

**账户检测自动化任务配置**

| 字段 | 类型 | 可空 | 说明 |
| --- | --- | --- | --- |
| `baseautomation_ptr_id` | CHAR(32) | 否 | baseautomation_ptr 的关联 ID |
| `engines` | LONGTEXT | 否 | Engines |

**索引：**

- PRIMARY KEY: baseautomation_ptr_id
- FK `accounts_checkaccoun_baseautomation_ptr_i_e32299f1_fk_assets_ba`: baseautomation_ptr_id → `assets_baseautomation`.id

---

### `accounts_checkaccountautomation_recipients`

**账户检测通知接收人**

| 字段 | 类型 | 可空 | 说明 |
| --- | --- | --- | --- |
| `id` | INT | 否 | 主键，UUID 格式（无连字符，32 位） |
| `checkaccountautomation_id` | CHAR(32) | 否 | checkaccountautomation 的关联 ID |
| `user_id` | CHAR(32) | 否 | 用户 ID |

**索引：**

- PRIMARY KEY: id
- UNIQUE `accounts_checkaccountaut_checkaccountautomation_i_9c3483a0_uniq`: checkaccountautomation_id,user_id
- INDEX `accounts_checkaccountaut_checkaccountautomation_i_9c3483a0_uniq`: checkaccountautomation_id,user_id
- INDEX `accounts_checkaccoun_user_id_4c868444_fk_users_use`: user_id
- FK `accounts_checkaccoun_checkaccountautomati_b695762e_fk_accounts_`: checkaccountautomation_id → `accounts_checkaccountautomation`.baseautomation_ptr_id
- FK `accounts_checkaccoun_user_id_4c868444_fk_users_use`: user_id → `users_user`.id

---

### `accounts_checkaccountengine`

**账户检测引擎配置**

| 字段 | 类型 | 可空 | 说明 |
| --- | --- | --- | --- |
| `created_by` | VARCHAR(128) | 是 | 创建者用户名 |
| `updated_by` | VARCHAR(128) | 是 | 最后更新者用户名 |
| `date_created` | DATETIME(6) | 是 | 创建时间 |
| `date_updated` | DATETIME(6) | 否 | 更新时间 |
| `comment` | LONGTEXT | 否 | 备注 |
| `id` | CHAR(32) | 否 | 主键，UUID 格式（无连字符，32 位） |
| `name` | VARCHAR(128) | 否 | Username |
| `slug` | VARCHAR(128) | 否 | Slug |

**索引：**

- PRIMARY KEY: id
- UNIQUE `name`: name
- UNIQUE `slug`: slug
- INDEX `name`: name
- INDEX `slug`: slug

---

### `accounts_gatheraccountsautomation`

**账户采集自动化任务配置**

| 字段 | 类型 | 可空 | 说明 |
| --- | --- | --- | --- |
| `baseautomation_ptr_id` | CHAR(32) | 否 | baseautomation_ptr 的关联 ID |
| `is_sync_account` | BOOLEAN | 否 | Sync Account标记 |
| `check_risk` | BOOLEAN | 否 | - |

**索引：**

- PRIMARY KEY: baseautomation_ptr_id
- FK `accounts_gatheraccou_baseautomation_ptr_i_365a6666_fk_assets_ba`: baseautomation_ptr_id → `assets_baseautomation`.id

---

### `accounts_gatheraccountsautomation_recipients`

**账户采集通知接收人**

| 字段 | 类型 | 可空 | 说明 |
| --- | --- | --- | --- |
| `id` | INT | 否 | 主键，UUID 格式（无连字符，32 位） |
| `gatheraccountsautomation_id` | CHAR(32) | 否 | gatheraccountsautomation 的关联 ID |
| `user_id` | CHAR(32) | 否 | 用户 ID |

**索引：**

- PRIMARY KEY: id
- UNIQUE `accounts_gatheraccountsa_gatheraccountsautomation_d785d290_uniq`: gatheraccountsautomation_id,user_id
- INDEX `accounts_gatheraccountsa_gatheraccountsautomation_d785d290_uniq`: gatheraccountsautomation_id,user_id
- INDEX `accounts_gatheraccou_user_id_50254711_fk_users_use`: user_id
- FK `accounts_gatheraccou_gatheraccountsautoma_fca5dd4d_fk_accounts_`: gatheraccountsautomation_id → `accounts_gatheraccountsautomation`.baseautomation_ptr_id
- FK `accounts_gatheraccou_user_id_50254711_fk_users_use`: user_id → `users_user`.id

---

### `accounts_gatheredaccount`

**采集到的账户记录**

| 字段 | 类型 | 可空 | 说明 |
| --- | --- | --- | --- |
| `created_by` | VARCHAR(128) | 是 | 创建者用户名 |
| `updated_by` | VARCHAR(128) | 是 | 最后更新者用户名 |
| `date_created` | DATETIME(6) | 是 | 创建时间 |
| `date_updated` | DATETIME(6) | 否 | 更新时间 |
| `comment` | LONGTEXT | 否 | 备注 |
| `id` | CHAR(32) | 否 | 主键，UUID 格式（无连字符，32 位） |
| `org_id` | VARCHAR(36) | 否 | 所属组织 ID，用于多租户数据隔离 |
| `present` | BOOLEAN | 否 | - |
| `date_last_login` | DATETIME(6) | 是 | Date last access |
| `username` | VARCHAR(128) | 否 | Username |
| `address_last_login` | VARCHAR(45) | 是 | - |
| `asset_id` | CHAR(32) | 否 | 关联资产 ID |
| `date_password_change` | DATETIME(6) | 是 | Password Change时间 |
| `date_password_expired` | DATETIME(6) | 是 | 密码过期时间 |
| `detail` | LONGTEXT | 否 | - |
| `remote_present` | BOOLEAN | 否 | - |
| `status` | VARCHAR(32) | 否 | Status |

**索引：**

- PRIMARY KEY: id
- UNIQUE `accounts_gatheredaccount_username_asset_id_1ae01c0f_uniq`: username,asset_id
- INDEX `accounts_gatheredaccount_username_asset_id_1ae01c0f_uniq`: username,asset_id
- INDEX `accounts_gatheredaccount_org_id_c8c5ae08`: org_id
- INDEX `accounts_gatheredaccount_username_0eedc6ee`: username
- INDEX `accounts_gatheredaccount_asset_id_710a010a_fk_assets_asset_id`: asset_id
- FK `accounts_gatheredaccount_asset_id_710a010a_fk_assets_asset_id`: asset_id → `assets_asset`.id

---

### `accounts_historicalaccount`

**历史账户记录（账户变更历史）**

| 字段 | 类型 | 可空 | 说明 |
| --- | --- | --- | --- |
| `id` | CHAR(32) | 否 | 主键，UUID 格式（无连字符，32 位） |
| `_secret` | LONGTEXT | 是 | 加密存储的密钥/密码 |
| `secret_type` | VARCHAR(16) | 否 | Secret type |
| `version` | INT | 否 | Version |
| `history_id` | INT | 否 | history 的关联 ID |
| `history_date` | DATETIME(6) | 否 | - |
| `history_change_reason` | VARCHAR(100) | 是 | - |
| `history_type` | VARCHAR(1) | 否 | - |
| `history_user_id` | CHAR(32) | 是 | history_user 的关联 ID |

**索引：**

- PRIMARY KEY: history_id
- INDEX `accounts_historicalaccount_id_5fcc9bec`: id
- INDEX `accounts_historicalaccount_history_date_316e758b`: history_date
- INDEX `accounts_historicala_history_user_id_882408fa_fk_users_use`: history_user_id
- FK `accounts_historicala_history_user_id_882408fa_fk_users_use`: history_user_id → `users_user`.id

---

### `accounts_integrationapplication`

**第三方集成应用配置**

| 字段 | 类型 | 可空 | 说明 |
| --- | --- | --- | --- |
| `created_by` | VARCHAR(128) | 是 | 创建者用户名 |
| `updated_by` | VARCHAR(128) | 是 | 最后更新者用户名 |
| `date_created` | DATETIME(6) | 是 | 创建时间 |
| `date_updated` | DATETIME(6) | 否 | 更新时间 |
| `comment` | LONGTEXT | 否 | 备注 |
| `id` | CHAR(32) | 否 | 主键，UUID 格式（无连字符，32 位） |
| `org_id` | VARCHAR(36) | 否 | 所属组织 ID，用于多租户数据隔离 |
| `name` | VARCHAR(128) | 否 | Username |
| `logo` | VARCHAR(128) | 否 | - |
| `secret` | LONGTEXT | 否 | 密钥/密码 |
| `accounts` | LONGTEXT | 否 | 授权账户 |
| `ip_group` | LONGTEXT | 否 | IP group |
| `date_last_used` | DATETIME(6) | 是 | Date last used |
| `is_active` | BOOLEAN | 否 | Active |

**索引：**

- PRIMARY KEY: id
- UNIQUE `accounts_integrationapplication_name_org_id_ff6c79fc_uniq`: name,org_id
- INDEX `accounts_integrationapplication_name_org_id_ff6c79fc_uniq`: name,org_id
- INDEX `accounts_integrationapplication_org_id_d32d418d`: org_id

---

### `accounts_pushaccountautomation`

**账户推送自动化任务配置**

| 字段 | 类型 | 可空 | 说明 |
| --- | --- | --- | --- |
| `baseautomation_ptr_id` | CHAR(32) | 否 | baseautomation_ptr 的关联 ID |
| `secret_type` | VARCHAR(16) | 否 | Secret type |
| `secret` | LONGTEXT | 是 | 密钥/密码 |
| `secret_strategy` | VARCHAR(16) | 否 | Secret strategy |
| `password_rules` | LONGTEXT | 否 | Password rules |
| `ssh_key_change_strategy` | VARCHAR(16) | 否 | SSH key change strategy |
| `check_conn_after_change` | BOOLEAN | 否 | Check connection after change |

**索引：**

- PRIMARY KEY: baseautomation_ptr_id
- FK `accounts_pushaccount_baseautomation_ptr_i_cabe9ea5_fk_assets_ba`: baseautomation_ptr_id → `assets_baseautomation`.id

---

### `accounts_pushsecretrecord`

**推送密码记录**

| 字段 | 类型 | 可空 | 说明 |
| --- | --- | --- | --- |
| `created_by` | VARCHAR(128) | 是 | 创建者用户名 |
| `updated_by` | VARCHAR(128) | 是 | 最后更新者用户名 |
| `date_created` | DATETIME(6) | 是 | 创建时间 |
| `date_updated` | DATETIME(6) | 否 | 更新时间 |
| `comment` | LONGTEXT | 否 | 备注 |
| `id` | CHAR(32) | 否 | 主键，UUID 格式（无连字符，32 位） |
| `date_finished` | DATETIME(6) | 是 | Date finished |
| `status` | VARCHAR(16) | 否 | Status |
| `error` | LONGTEXT | 是 | Error |
| `account_id` | CHAR(32) | 是 | account 的关联 ID |
| `asset_id` | CHAR(32) | 是 | 关联资产 ID |
| `execution_id` | CHAR(32) | 是 | 执行记录 ID |

**索引：**

- PRIMARY KEY: id
- INDEX `accounts_pushsecretr_account_id_dc8fe7b8_fk_accounts_`: account_id
- INDEX `accounts_pushsecretrecord_asset_id_1942df32_fk_assets_asset_id`: asset_id
- INDEX `accounts_pushsecretr_execution_id_7c0a7bd3_fk_assets_au`: execution_id
- INDEX `accounts_pushsecretrecord_date_finished_7398fb1f`: date_finished
- FK `accounts_pushsecretr_account_id_dc8fe7b8_fk_accounts_`: account_id → `accounts_account`.id
- FK `accounts_pushsecretr_execution_id_7c0a7bd3_fk_assets_au`: execution_id → `assets_automationexecution`.id
- FK `accounts_pushsecretrecord_asset_id_1942df32_fk_assets_asset_id`: asset_id → `assets_asset`.id

---

### `accounts_verifyaccountautomation`

**账户验证自动化任务配置**

| 字段 | 类型 | 可空 | 说明 |
| --- | --- | --- | --- |
| `baseautomation_ptr_id` | CHAR(32) | 否 | baseautomation_ptr 的关联 ID |

**索引：**

- PRIMARY KEY: baseautomation_ptr_id
- FK `accounts_verifyaccou_baseautomation_ptr_i_318f0963_fk_assets_ba`: baseautomation_ptr_id → `assets_baseautomation`.id

---

### `accounts_virtualaccount`

**虚拟账户（运行时临时生成的账户）**

| 字段 | 类型 | 可空 | 说明 |
| --- | --- | --- | --- |
| `created_by` | VARCHAR(128) | 是 | 创建者用户名 |
| `updated_by` | VARCHAR(128) | 是 | 最后更新者用户名 |
| `date_created` | DATETIME(6) | 是 | 创建时间 |
| `date_updated` | DATETIME(6) | 否 | 更新时间 |
| `id` | CHAR(32) | 否 | 主键，UUID 格式（无连字符，32 位） |
| `org_id` | VARCHAR(36) | 否 | 所属组织 ID，用于多租户数据隔离 |
| `alias` | VARCHAR(128) | 否 | Alias |
| `secret_from_login` | BOOLEAN | 是 | Virtual account |

**索引：**

- PRIMARY KEY: id
- UNIQUE `accounts_virtualaccount_alias_org_id_847a87d6_uniq`: alias,org_id
- INDEX `accounts_virtualaccount_alias_org_id_847a87d6_uniq`: alias,org_id
- INDEX `accounts_virtualaccount_org_id_6ae8edaa`: org_id

---

## 访问控制（ACLs）

基于 ACL 的细粒度访问控制，包括命令过滤、登录限制、数据脱敏等

### `acls_commandfilteracl`

**命令过滤 ACL 规则，控制用户可执行的命令范围**

| 字段 | 类型 | 可空 | 说明 |
| --- | --- | --- | --- |
| `created_by` | VARCHAR(128) | 是 | 创建者用户名 |
| `updated_by` | VARCHAR(128) | 是 | 最后更新者用户名 |
| `date_created` | DATETIME(6) | 是 | 创建时间 |
| `date_updated` | DATETIME(6) | 否 | 更新时间 |
| `comment` | LONGTEXT | 否 | 备注 |
| `id` | CHAR(32) | 否 | 主键，UUID 格式（无连字符，32 位） |
| `org_id` | VARCHAR(36) | 否 | 所属组织 ID，用于多租户数据隔离 |
| `priority` | INT | 否 | Action |
| `action` | VARCHAR(64) | 否 | Action |
| `is_active` | BOOLEAN | 否 | 是否启用 |
| `users` | LONGTEXT | 否 | 授权用户 |
| `name` | VARCHAR(128) | 否 | Name |
| `assets` | LONGTEXT | 否 | 授权资产 |
| `accounts` | LONGTEXT | 否 | 授权账户 |

**索引：**

- PRIMARY KEY: id
- UNIQUE `acls_commandfilteracl_name_org_id_00af4220_uniq`: name,org_id
- INDEX `acls_commandfilteracl_name_org_id_00af4220_uniq`: name,org_id
- INDEX `acls_commandfilteracl_org_id_b8fbeff4`: org_id

---

### `acls_commandfilteracl_command_groups`

**命令过滤 ACL 与命令组的多对多关联**

| 字段 | 类型 | 可空 | 说明 |
| --- | --- | --- | --- |
| `id` | INT | 否 | 主键，UUID 格式（无连字符，32 位） |
| `commandfilteracl_id` | CHAR(32) | 否 | commandfilteracl 的关联 ID |
| `commandgroup_id` | CHAR(32) | 否 | commandgroup 的关联 ID |

**索引：**

- PRIMARY KEY: id
- UNIQUE `acls_commandfilteracl_co_commandfilteracl_id_comm_3c4e6e95_uniq`: commandfilteracl_id,commandgroup_id
- INDEX `acls_commandfilteracl_co_commandfilteracl_id_comm_3c4e6e95_uniq`: commandfilteracl_id,commandgroup_id
- INDEX `acls_commandfilterac_commandgroup_id_9d91146b_fk_acls_comm`: commandgroup_id
- FK `acls_commandfilterac_commandfilteracl_id_ac7ca31f_fk_acls_comm`: commandfilteracl_id → `acls_commandfilteracl`.id
- FK `acls_commandfilterac_commandgroup_id_9d91146b_fk_acls_comm`: commandgroup_id → `acls_commandgroup`.id

---

### `acls_commandfilteracl_reviewers`

**命令过滤 ACL 审批人**

| 字段 | 类型 | 可空 | 说明 |
| --- | --- | --- | --- |
| `id` | INT | 否 | 主键，UUID 格式（无连字符，32 位） |
| `commandfilteracl_id` | CHAR(32) | 否 | commandfilteracl 的关联 ID |
| `user_id` | CHAR(32) | 否 | 用户 ID |

**索引：**

- PRIMARY KEY: id
- UNIQUE `acls_commandfilteracl_re_commandfilteracl_id_user_b4d70d79_uniq`: commandfilteracl_id,user_id
- INDEX `acls_commandfilteracl_re_commandfilteracl_id_user_b4d70d79_uniq`: commandfilteracl_id,user_id
- INDEX `acls_commandfilterac_user_id_deb79bbc_fk_users_use`: user_id
- FK `acls_commandfilterac_commandfilteracl_id_2c7001a2_fk_acls_comm`: commandfilteracl_id → `acls_commandfilteracl`.id
- FK `acls_commandfilterac_user_id_deb79bbc_fk_users_use`: user_id → `users_user`.id

---

### `acls_commandgroup`

**命令组，定义一组可被过滤的命令**

| 字段 | 类型 | 可空 | 说明 |
| --- | --- | --- | --- |
| `created_by` | VARCHAR(128) | 是 | 创建者用户名 |
| `updated_by` | VARCHAR(128) | 是 | 最后更新者用户名 |
| `date_created` | DATETIME(6) | 是 | 创建时间 |
| `date_updated` | DATETIME(6) | 否 | 更新时间 |
| `comment` | LONGTEXT | 否 | 备注 |
| `id` | CHAR(32) | 否 | 主键，UUID 格式（无连字符，32 位） |
| `org_id` | VARCHAR(36) | 否 | 所属组织 ID，用于多租户数据隔离 |
| `name` | VARCHAR(128) | 否 | Name |
| `type` | VARCHAR(16) | 否 | Ignore case |
| `content` | LONGTEXT | 否 | Ignore case |
| `ignore_case` | BOOLEAN | 否 | Ignore case |

**索引：**

- PRIMARY KEY: id
- UNIQUE `acls_commandgroup_org_id_name_3d9df455_uniq`: org_id,name
- INDEX `acls_commandgroup_org_id_name_3d9df455_uniq`: org_id,name
- INDEX `acls_commandgroup_org_id_b5b46362`: org_id

---

### `acls_connectmethodacl`

**连接方式 ACL 规则，控制允许使用的连接方式**

| 字段 | 类型 | 可空 | 说明 |
| --- | --- | --- | --- |
| `created_by` | VARCHAR(128) | 是 | 创建者用户名 |
| `updated_by` | VARCHAR(128) | 是 | 最后更新者用户名 |
| `date_created` | DATETIME(6) | 是 | 创建时间 |
| `date_updated` | DATETIME(6) | 否 | 更新时间 |
| `comment` | LONGTEXT | 否 | 备注 |
| `id` | CHAR(32) | 否 | 主键，UUID 格式（无连字符，32 位） |
| `name` | VARCHAR(128) | 否 | Name |
| `priority` | INT | 否 | Action |
| `action` | VARCHAR(64) | 否 | Action |
| `is_active` | BOOLEAN | 否 | 是否启用 |
| `users` | LONGTEXT | 否 | 授权用户 |
| `connect_methods` | LONGTEXT | 否 | Connect methods |

**索引：**

- PRIMARY KEY: id
- UNIQUE `name`: name
- INDEX `name`: name

---

### `acls_connectmethodacl_reviewers`

**连接方式 ACL 审批人**

| 字段 | 类型 | 可空 | 说明 |
| --- | --- | --- | --- |
| `id` | INT | 否 | 主键，UUID 格式（无连字符，32 位） |
| `connectmethodacl_id` | CHAR(32) | 否 | connectmethodacl 的关联 ID |
| `user_id` | CHAR(32) | 否 | 用户 ID |

**索引：**

- PRIMARY KEY: id
- UNIQUE `acls_connectmethodacl_re_connectmethodacl_id_user_12f32736_uniq`: connectmethodacl_id,user_id
- INDEX `acls_connectmethodacl_re_connectmethodacl_id_user_12f32736_uniq`: connectmethodacl_id,user_id
- INDEX `acls_connectmethodac_user_id_10422014_fk_users_use`: user_id
- FK `acls_connectmethodac_connectmethodacl_id_02a7e52a_fk_acls_conn`: connectmethodacl_id → `acls_connectmethodacl`.id
- FK `acls_connectmethodac_user_id_10422014_fk_users_use`: user_id → `users_user`.id

---

### `acls_datamaskingrule`

**数据脱敏规则，定义敏感数据的脱敏方式**

| 字段 | 类型 | 可空 | 说明 |
| --- | --- | --- | --- |
| `created_by` | VARCHAR(128) | 是 | 创建者用户名 |
| `updated_by` | VARCHAR(128) | 是 | 最后更新者用户名 |
| `date_created` | DATETIME(6) | 是 | 创建时间 |
| `date_updated` | DATETIME(6) | 否 | 更新时间 |
| `comment` | LONGTEXT | 否 | 备注 |
| `id` | CHAR(32) | 否 | 主键，UUID 格式（无连字符，32 位） |
| `org_id` | VARCHAR(36) | 否 | 所属组织 ID，用于多租户数据隔离 |
| `priority` | INT | 否 | Action |
| `action` | VARCHAR(64) | 否 | Action |
| `is_active` | BOOLEAN | 否 | 是否启用 |
| `users` | LONGTEXT | 否 | 授权用户 |
| `assets` | LONGTEXT | 否 | 授权资产 |
| `accounts` | LONGTEXT | 否 | 授权账户 |
| `name` | VARCHAR(128) | 否 | Name |
| `fields_pattern` | VARCHAR(128) | 否 | - |
| `masking_method` | VARCHAR(32) | 否 | - |
| `mask_pattern` | VARCHAR(128) | 是 | - |

**索引：**

- PRIMARY KEY: id
- UNIQUE `acls_datamaskingrule_org_id_name_ee135890_uniq`: org_id,name
- INDEX `acls_datamaskingrule_org_id_name_ee135890_uniq`: org_id,name
- INDEX `acls_datamaskingrule_org_id_f2adda4f`: org_id

---

### `acls_datamaskingrule_reviewers`

**数据脱敏规则审批人**

| 字段 | 类型 | 可空 | 说明 |
| --- | --- | --- | --- |
| `id` | INT | 否 | 主键，UUID 格式（无连字符，32 位） |
| `datamaskingrule_id` | CHAR(32) | 否 | datamaskingrule 的关联 ID |
| `user_id` | CHAR(32) | 否 | 用户 ID |

**索引：**

- PRIMARY KEY: id
- UNIQUE `acls_datamaskingrule_rev_datamaskingrule_id_user__f998bfbc_uniq`: datamaskingrule_id,user_id
- INDEX `acls_datamaskingrule_rev_datamaskingrule_id_user__f998bfbc_uniq`: datamaskingrule_id,user_id
- INDEX `acls_datamaskingrule_reviewers_user_id_2596c860_fk_users_user_id`: user_id
- FK `acls_datamaskingrule_datamaskingrule_id_fe6298cb_fk_acls_data`: datamaskingrule_id → `acls_datamaskingrule`.id
- FK `acls_datamaskingrule_reviewers_user_id_2596c860_fk_users_user_id`: user_id → `users_user`.id

---

### `acls_loginacl`

**登录 ACL 规则，控制用户登录条件（时间/IP/MFA 等）**

| 字段 | 类型 | 可空 | 说明 |
| --- | --- | --- | --- |
| `created_by` | VARCHAR(128) | 是 | 创建者用户名 |
| `updated_by` | VARCHAR(128) | 是 | 最后更新者用户名 |
| `date_created` | DATETIME(6) | 是 | 创建时间 |
| `date_updated` | DATETIME(6) | 否 | 更新时间 |
| `comment` | LONGTEXT | 否 | 备注 |
| `id` | CHAR(32) | 否 | 主键，UUID 格式（无连字符，32 位） |
| `name` | VARCHAR(128) | 否 | Name |
| `priority` | INT | 否 | Action |
| `action` | VARCHAR(64) | 否 | Action |
| `is_active` | BOOLEAN | 否 | 是否启用 |
| `users` | LONGTEXT | 否 | 授权用户 |
| `rules` | LONGTEXT | 否 | Rule |

**索引：**

- PRIMARY KEY: id
- UNIQUE `name`: name
- INDEX `name`: name

---

### `acls_loginacl_reviewers`

**登录 ACL 审批人**

| 字段 | 类型 | 可空 | 说明 |
| --- | --- | --- | --- |
| `id` | INT | 否 | 主键，UUID 格式（无连字符，32 位） |
| `loginacl_id` | CHAR(32) | 否 | loginacl 的关联 ID |
| `user_id` | CHAR(32) | 否 | 用户 ID |

**索引：**

- PRIMARY KEY: id
- UNIQUE `acls_loginacl_reviewers_loginacl_id_user_id_f5316a9b_uniq`: loginacl_id,user_id
- INDEX `acls_loginacl_reviewers_loginacl_id_user_id_f5316a9b_uniq`: loginacl_id,user_id
- INDEX `acls_loginacl_reviewers_user_id_9ab0d726_fk_users_user_id`: user_id
- FK `acls_loginacl_reviewers_loginacl_id_79f293a0_fk_acls_loginacl_id`: loginacl_id → `acls_loginacl`.id
- FK `acls_loginacl_reviewers_user_id_9ab0d726_fk_users_user_id`: user_id → `users_user`.id

---

### `acls_loginassetacl`

**登录资产 ACL 规则，控制用户可登录的资产范围**

| 字段 | 类型 | 可空 | 说明 |
| --- | --- | --- | --- |
| `created_by` | VARCHAR(128) | 是 | 创建者用户名 |
| `updated_by` | VARCHAR(128) | 是 | 最后更新者用户名 |
| `date_created` | DATETIME(6) | 是 | 创建时间 |
| `date_updated` | DATETIME(6) | 否 | 更新时间 |
| `comment` | LONGTEXT | 否 | 备注 |
| `id` | CHAR(32) | 否 | 主键，UUID 格式（无连字符，32 位） |
| `org_id` | VARCHAR(36) | 否 | 所属组织 ID，用于多租户数据隔离 |
| `priority` | INT | 否 | Action |
| `action` | VARCHAR(64) | 否 | Action |
| `is_active` | BOOLEAN | 否 | 是否启用 |
| `users` | LONGTEXT | 否 | 授权用户 |
| `name` | VARCHAR(128) | 否 | Name |
| `assets` | LONGTEXT | 否 | 授权资产 |
| `accounts` | LONGTEXT | 否 | 授权账户 |
| `rules` | LONGTEXT | 否 | Rule |

**索引：**

- PRIMARY KEY: id
- UNIQUE `acls_loginassetacl_name_org_id_59405bfe_uniq`: name,org_id
- INDEX `acls_loginassetacl_name_org_id_59405bfe_uniq`: name,org_id
- INDEX `acls_loginassetacl_org_id_3ff345c7`: org_id

---

### `acls_loginassetacl_reviewers`

**登录资产 ACL 审批人**

| 字段 | 类型 | 可空 | 说明 |
| --- | --- | --- | --- |
| `id` | INT | 否 | 主键，UUID 格式（无连字符，32 位） |
| `loginassetacl_id` | CHAR(32) | 否 | loginassetacl 的关联 ID |
| `user_id` | CHAR(32) | 否 | 用户 ID |

**索引：**

- PRIMARY KEY: id
- UNIQUE `acls_loginassetacl_revie_loginassetacl_id_user_id_d4269138_uniq`: loginassetacl_id,user_id
- INDEX `acls_loginassetacl_revie_loginassetacl_id_user_id_d4269138_uniq`: loginassetacl_id,user_id
- INDEX `acls_loginassetacl_reviewers_user_id_9b8bcd8d_fk_users_user_id`: user_id
- FK `acls_loginassetacl_r_loginassetacl_id_4e95e191_fk_acls_logi`: loginassetacl_id → `acls_loginassetacl`.id
- FK `acls_loginassetacl_reviewers_user_id_9b8bcd8d_fk_users_user_id`: user_id → `users_user`.id

---

## 资产管理（Assets）

管理所有受管资产，包括主机、数据库、网络设备、Web 应用等

### `assets_asset`

**资产信息主表，存储所有受管资产（主机/数据库/设备/Web 等）**

| 字段 | 类型 | 可空 | 说明 |
| --- | --- | --- | --- |
| `created_by` | VARCHAR(128) | 是 | Created by |
| `updated_by` | VARCHAR(128) | 是 | 最后更新者用户名 |
| `date_created` | DATETIME(6) | 是 | Created by |
| `date_updated` | DATETIME(6) | 否 | Created by |
| `comment` | LONGTEXT | 否 | Created by |
| `id` | CHAR(32) | 否 | Full value |
| `org_id` | VARCHAR(36) | 否 | 所属组织 ID，用于多租户数据隔离 |
| `connectivity` | VARCHAR(16) | 否 | Connectivity |
| `date_verified` | DATETIME(6) | 是 | 最后验证时间 |
| `name` | VARCHAR(128) | 否 | Name |
| `address` | VARCHAR(767) | 否 | Address |
| `is_active` | BOOLEAN | 否 | Last execution date |
| `gathered_info` | LONGTEXT | 否 | Gathered info |
| `custom_info` | LONGTEXT | 否 | Custom info |
| `zone_id` | CHAR(32) | 是 | zone 的关联 ID |
| `platform_id` | INT | 否 | platform 的关联 ID |

**索引：**

- PRIMARY KEY: id
- UNIQUE `assets_asset_org_id_name_f861452a_uniq`: org_id,name
- INDEX `assets_asset_org_id_name_f861452a_uniq`: org_id,name
- INDEX `assets_asset_org_id_f25200c7`: org_id
- INDEX `assets_asset_address_b40a50bd`: address
- INDEX `assets_asset_platform_id_b2b0830c_fk_assets_platform_id`: platform_id
- INDEX `assets_asset_zone_id_0e4b6342_fk_assets_zone_id`: zone_id
- FK `assets_asset_platform_id_b2b0830c_fk_assets_platform_id`: platform_id → `assets_platform`.id
- FK `assets_asset_zone_id_0e4b6342_fk_assets_zone_id`: zone_id → `assets_zone`.id

---

### `assets_asset_directory_services`

**资产与目录服务（AD/LDAP）的多对多关联**

| 字段 | 类型 | 可空 | 说明 |
| --- | --- | --- | --- |
| `id` | INT | 否 | Full value |
| `asset_id` | CHAR(32) | 否 | 关联资产 ID |
| `directoryservice_id` | CHAR(32) | 否 | directoryservice 的关联 ID |

**索引：**

- PRIMARY KEY: id
- UNIQUE `assets_asset_directory_s_asset_id_directoryservic_36854334_uniq`: asset_id,directoryservice_id
- INDEX `assets_asset_directory_s_asset_id_directoryservic_36854334_uniq`: asset_id,directoryservice_id
- INDEX `assets_asset_directo_directoryservice_id_daf6d48e_fk_assets_di`: directoryservice_id
- FK `assets_asset_directo_asset_id_9ff3def8_fk_assets_as`: asset_id → `assets_asset`.id
- FK `assets_asset_directo_directoryservice_id_daf6d48e_fk_assets_di`: directoryservice_id → `assets_directoryservice`.asset_ptr_id

---

### `assets_asset_nodes`

**资产与节点的多对多关联**

| 字段 | 类型 | 可空 | 说明 |
| --- | --- | --- | --- |
| `id` | INT | 否 | Full value |
| `asset_id` | CHAR(32) | 否 | 关联资产 ID |
| `node_id` | CHAR(32) | 否 | node 的关联 ID |

**索引：**

- PRIMARY KEY: id
- UNIQUE `assets_asset_nodes_asset_id_node_id_f4aa1161_uniq`: asset_id,node_id
- INDEX `assets_asset_nodes_asset_id_node_id_f4aa1161_uniq`: asset_id,node_id
- INDEX `assets_asset_nodes_node_id_bfe6279c_fk_assets_node_id`: node_id
- FK `assets_asset_nodes_asset_id_8f05f3ee_fk_assets_asset_id`: asset_id → `assets_asset`.id
- FK `assets_asset_nodes_node_id_bfe6279c_fk_assets_node_id`: node_id → `assets_node`.id

---

### `assets_automationexecution`

**自动化任务执行记录**

| 字段 | 类型 | 可空 | 说明 |
| --- | --- | --- | --- |
| `org_id` | VARCHAR(36) | 否 | 所属组织 ID，用于多租户数据隔离 |
| `id` | CHAR(32) | 否 | Full value |
| `status` | VARCHAR(16) | 否 | 状态 |
| `date_created` | DATETIME(6) | 否 | Created by |
| `date_start` | DATETIME(6) | 是 | 开始时间 |
| `date_finished` | DATETIME(6) | 是 | Finished时间 |
| `snapshot` | LONGTEXT | 是 | - |
| `trigger` | VARCHAR(128) | 否 | - |
| `automation_id` | CHAR(32) | 是 | automation 的关联 ID |
| `result` | LONGTEXT | 否 | 结果 |
| `summary` | LONGTEXT | 否 | - |
| `type` | VARCHAR(32) | 否 | Last execution date |

**索引：**

- PRIMARY KEY: id
- INDEX `assets_automationexecution_org_id_a68372e6`: org_id
- INDEX `assets_automationexecution_date_start_87e25a00`: date_start
- INDEX `assets_automationexe_automation_id_9e4a308b_fk_assets_ba`: automation_id
- FK `assets_automationexe_automation_id_9e4a308b_fk_assets_ba`: automation_id → `assets_baseautomation`.id

---

### `assets_baseautomation`

**基础自动化任务配置（Ping/采集/推送等）**

| 字段 | 类型 | 可空 | 说明 |
| --- | --- | --- | --- |
| `created_by` | VARCHAR(128) | 是 | Created by |
| `updated_by` | VARCHAR(128) | 是 | 最后更新者用户名 |
| `date_created` | DATETIME(6) | 是 | Created by |
| `date_updated` | DATETIME(6) | 否 | Created by |
| `comment` | LONGTEXT | 否 | Created by |
| `id` | CHAR(32) | 否 | Full value |
| `org_id` | VARCHAR(36) | 否 | 所属组织 ID，用于多租户数据隔离 |
| `name` | VARCHAR(128) | 否 | Name |
| `is_periodic` | BOOLEAN | 否 | Periodic标记 |
| `interval` | INT | 是 | - |
| `crontab` | VARCHAR(128) | 否 | - |
| `accounts` | LONGTEXT | 否 | Is active |
| `type` | VARCHAR(16) | 否 | Last execution date |
| `is_active` | BOOLEAN | 否 | Last execution date |
| `params` | LONGTEXT | 否 | Last execution date |
| `start_time` | DATETIME(6) | 是 | - |
| `date_last_run` | DATETIME(6) | 是 | Last Run时间 |
| `last_execution_date` | DATETIME(6) | 是 | Last execution date |

**索引：**

- PRIMARY KEY: id
- UNIQUE `assets_baseautomation_org_id_name_type_7abb1169_uniq`: org_id,name,type
- INDEX `assets_baseautomation_org_id_name_type_7abb1169_uniq`: org_id,name,type
- INDEX `assets_baseautomation_org_id_90cdbb4e`: org_id

---

### `assets_baseautomation_assets`

**自动化任务与资产的多对多关联**

| 字段 | 类型 | 可空 | 说明 |
| --- | --- | --- | --- |
| `id` | INT | 否 | Full value |
| `baseautomation_id` | CHAR(32) | 否 | baseautomation 的关联 ID |
| `asset_id` | CHAR(32) | 否 | 关联资产 ID |

**索引：**

- PRIMARY KEY: id
- UNIQUE `assets_baseautomation_as_baseautomation_id_asset__c61bf0b9_uniq`: baseautomation_id,asset_id
- INDEX `assets_baseautomation_as_baseautomation_id_asset__c61bf0b9_uniq`: baseautomation_id,asset_id
- INDEX `assets_baseautomatio_asset_id_0704a331_fk_assets_as`: asset_id
- FK `assets_baseautomatio_asset_id_0704a331_fk_assets_as`: asset_id → `assets_asset`.id
- FK `assets_baseautomatio_baseautomation_id_39e8581c_fk_assets_ba`: baseautomation_id → `assets_baseautomation`.id

---

### `assets_baseautomation_nodes`

**自动化任务与节点的多对多关联**

| 字段 | 类型 | 可空 | 说明 |
| --- | --- | --- | --- |
| `id` | INT | 否 | Full value |
| `baseautomation_id` | CHAR(32) | 否 | baseautomation 的关联 ID |
| `node_id` | CHAR(32) | 否 | node 的关联 ID |

**索引：**

- PRIMARY KEY: id
- UNIQUE `assets_baseautomation_no_baseautomation_id_node_i_bd718cde_uniq`: baseautomation_id,node_id
- INDEX `assets_baseautomation_no_baseautomation_id_node_i_bd718cde_uniq`: baseautomation_id,node_id
- INDEX `assets_baseautomation_nodes_node_id_11df5b5b_fk_assets_node_id`: node_id
- FK `assets_baseautomatio_baseautomation_id_5c9eea85_fk_assets_ba`: baseautomation_id → `assets_baseautomation`.id
- FK `assets_baseautomation_nodes_node_id_11df5b5b_fk_assets_node_id`: node_id → `assets_node`.id

---

### `assets_cloud`

**云资产（由云同步自动创建的资产）**

| 字段 | 类型 | 可空 | 说明 |
| --- | --- | --- | --- |
| `asset_ptr_id` | CHAR(32) | 否 | asset_ptr 的关联 ID |

**索引：**

- PRIMARY KEY: asset_ptr_id
- FK `assets_cloud_asset_ptr_id_44d12f5e_fk_assets_asset_id`: asset_ptr_id → `assets_asset`.id

---

### `assets_custom`

**自定义资产（用户手动创建的资产）**

| 字段 | 类型 | 可空 | 说明 |
| --- | --- | --- | --- |
| `asset_ptr_id` | CHAR(32) | 否 | asset_ptr 的关联 ID |

**索引：**

- PRIMARY KEY: asset_ptr_id
- FK `assets_custom_asset_ptr_id_c9ab0d9d_fk_assets_asset_id`: asset_ptr_id → `assets_asset`.id

---

### `assets_database`

**数据库资产（MySQL/PostgreSQL/Redis 等）**

| 字段 | 类型 | 可空 | 说明 |
| --- | --- | --- | --- |
| `asset_ptr_id` | CHAR(32) | 否 | asset_ptr 的关联 ID |
| `db_name` | VARCHAR(1024) | 否 | Allow invalid cert |
| `use_ssl` | BOOLEAN | 否 | Allow invalid cert |
| `ca_cert` | LONGTEXT | 否 | - |
| `client_cert` | LONGTEXT | 否 | - |
| `client_key` | LONGTEXT | 否 | - |
| `allow_invalid_cert` | BOOLEAN | 否 | Allow invalid cert |
| `pg_ssl_mode` | VARCHAR(16) | 否 | Postgresql SSL mode |

**索引：**

- PRIMARY KEY: asset_ptr_id
- FK `assets_database_asset_ptr_id_cbfecc96_fk_assets_asset_id`: asset_ptr_id → `assets_asset`.id

---

### `assets_device`

**网络设备资产（交换机/路由器/防火墙等）**

| 字段 | 类型 | 可空 | 说明 |
| --- | --- | --- | --- |
| `asset_ptr_id` | CHAR(32) | 否 | asset_ptr 的关联 ID |

**索引：**

- PRIMARY KEY: asset_ptr_id
- FK `assets_device_asset_ptr_id_fc7eff6e_fk_assets_asset_id`: asset_ptr_id → `assets_asset`.id

---

### `assets_directoryservice`

**目录服务配置（AD/LDAP 集成）**

| 字段 | 类型 | 可空 | 说明 |
| --- | --- | --- | --- |
| `asset_ptr_id` | CHAR(32) | 否 | asset_ptr 的关联 ID |
| `domain_name` | VARCHAR(128) | 否 | - |

**索引：**

- PRIMARY KEY: asset_ptr_id
- FK `assets_directoryservice_asset_ptr_id_b9e18d35_fk_assets_asset_id`: asset_ptr_id → `assets_asset`.id

---

### `assets_favoriteasset`

**用户收藏的资产**

| 字段 | 类型 | 可空 | 说明 |
| --- | --- | --- | --- |
| `created_by` | VARCHAR(128) | 是 | Created by |
| `updated_by` | VARCHAR(128) | 是 | 最后更新者用户名 |
| `date_created` | DATETIME(6) | 是 | Created by |
| `date_updated` | DATETIME(6) | 否 | Created by |
| `comment` | LONGTEXT | 否 | Created by |
| `id` | CHAR(32) | 否 | Full value |
| `asset_id` | CHAR(32) | 否 | 关联资产 ID |
| `user_id` | CHAR(32) | 否 | 用户 ID |
| `folder_id` | CHAR(32) | 是 | folder 的关联 ID |

**索引：**

- PRIMARY KEY: id
- UNIQUE `assets_favoriteasset_user_id_asset_id_872412e3_uniq`: user_id,asset_id
- INDEX `assets_favoriteasset_user_id_asset_id_872412e3_uniq`: user_id,asset_id
- INDEX `assets_favoriteasset_asset_id_ac2ed019_fk_assets_asset_id`: asset_id
- INDEX `assets_favoriteasset_folder_id_f89b44cb_fk_assets_fa`: folder_id
- FK `assets_favoriteasset_asset_id_ac2ed019_fk_assets_asset_id`: asset_id → `assets_asset`.id
- FK `assets_favoriteasset_folder_id_f89b44cb_fk_assets_fa`: folder_id → `assets_favoritefolder`.id
- FK `assets_favoriteasset_user_id_7809bc5b_fk_users_user_id`: user_id → `users_user`.id

---

### `assets_favoritefolder`

**用户收藏的文件夹**

| 字段 | 类型 | 可空 | 说明 |
| --- | --- | --- | --- |
| `created_by` | VARCHAR(128) | 是 | Created by |
| `updated_by` | VARCHAR(128) | 是 | 最后更新者用户名 |
| `date_created` | DATETIME(6) | 是 | Created by |
| `date_updated` | DATETIME(6) | 否 | Created by |
| `comment` | LONGTEXT | 否 | Created by |
| `id` | CHAR(32) | 否 | Full value |
| `name` | VARCHAR(128) | 否 | Name |
| `parent_id` | CHAR(32) | 是 | 父级 ID |
| `user_id` | CHAR(32) | 否 | 用户 ID |

**索引：**

- PRIMARY KEY: id
- UNIQUE `assets_favoritefolder_user_id_name_parent_id_08ff5284_uniq`: user_id,name,parent_id
- INDEX `assets_favoritefolder_user_id_name_parent_id_08ff5284_uniq`: user_id,name,parent_id
- INDEX `assets_favoritefolde_parent_id_8dacb57d_fk_assets_fa`: parent_id
- FK `assets_favoritefolde_parent_id_8dacb57d_fk_assets_fa`: parent_id → `assets_favoritefolder`.id
- FK `assets_favoritefolder_user_id_515f17f2_fk_users_user_id`: user_id → `users_user`.id

---

### `assets_gatherfactsautomation`

**资产信息采集自动化任务**

| 字段 | 类型 | 可空 | 说明 |
| --- | --- | --- | --- |
| `baseautomation_ptr_id` | CHAR(32) | 否 | baseautomation_ptr 的关联 ID |

**索引：**

- PRIMARY KEY: baseautomation_ptr_id
- FK `assets_gatherfactsau_baseautomation_ptr_i_4f797d64_fk_assets_ba`: baseautomation_ptr_id → `assets_baseautomation`.id

---

### `assets_gpt`

**GPT 集成配置**

| 字段 | 类型 | 可空 | 说明 |
| --- | --- | --- | --- |
| `asset_ptr_id` | CHAR(32) | 否 | asset_ptr 的关联 ID |
| `proxy` | VARCHAR(128) | 否 | - |

**索引：**

- PRIMARY KEY: asset_ptr_id
- FK `assets_gpt_asset_ptr_id_b92bbec5_fk_assets_asset_id`: asset_ptr_id → `assets_asset`.id

---

### `assets_host`

**主机资产（Linux/Windows 服务器）**

| 字段 | 类型 | 可空 | 说明 |
| --- | --- | --- | --- |
| `asset_ptr_id` | CHAR(32) | 否 | asset_ptr 的关联 ID |

**索引：**

- PRIMARY KEY: asset_ptr_id
- FK `assets_host_asset_ptr_id_d0801966_fk_assets_asset_id`: asset_ptr_id → `assets_asset`.id

---

### `assets_label`

**标签定义**

| 字段 | 类型 | 可空 | 说明 |
| --- | --- | --- | --- |
| `created_by` | VARCHAR(128) | 是 | Created by |
| `updated_by` | VARCHAR(128) | 是 | 最后更新者用户名 |
| `date_created` | DATETIME(6) | 是 | Created by |
| `date_updated` | DATETIME(6) | 否 | Created by |
| `comment` | LONGTEXT | 否 | Created by |
| `id` | CHAR(32) | 否 | Full value |
| `org_id` | VARCHAR(36) | 否 | 所属组织 ID，用于多租户数据隔离 |
| `name` | VARCHAR(128) | 否 | Name |
| `value` | VARCHAR(128) | 否 | Full value |
| `category` | VARCHAR(128) | 否 | - |
| `is_active` | BOOLEAN | 否 | Last execution date |

**索引：**

- PRIMARY KEY: id
- UNIQUE `assets_label_name_value_org_id_ca0b35a2_uniq`: name,value,org_id
- INDEX `assets_label_name_value_org_id_ca0b35a2_uniq`: name,value,org_id
- INDEX `assets_label_org_id_2a425d25`: org_id

---

### `assets_myasset`

**我的资产（用户自定义资产视图）**

| 字段 | 类型 | 可空 | 说明 |
| --- | --- | --- | --- |
| `created_by` | VARCHAR(128) | 是 | Created by |
| `updated_by` | VARCHAR(128) | 是 | 最后更新者用户名 |
| `date_created` | DATETIME(6) | 是 | Created by |
| `date_updated` | DATETIME(6) | 否 | Created by |
| `id` | CHAR(32) | 否 | Full value |
| `name` | VARCHAR(128) | 否 | Name |
| `comment` | VARCHAR(512) | 否 | Created by |
| `asset_id` | CHAR(32) | 否 | 关联资产 ID |
| `user_id` | CHAR(32) | 否 | 用户 ID |

**索引：**

- PRIMARY KEY: id
- UNIQUE `assets_myasset_user_id_asset_id_d2fd9886_uniq`: user_id,asset_id
- INDEX `assets_myasset_user_id_asset_id_d2fd9886_uniq`: user_id,asset_id
- INDEX `assets_myasset_asset_id_eff8cabd_fk_assets_asset_id`: asset_id
- FK `assets_myasset_asset_id_eff8cabd_fk_assets_asset_id`: asset_id → `assets_asset`.id
- FK `assets_myasset_user_id_637b61f7_fk_users_user_id`: user_id → `users_user`.id

---

### `assets_node`

**资产节点（树形组织结构）**

| 字段 | 类型 | 可空 | 说明 |
| --- | --- | --- | --- |
| `created_by` | VARCHAR(128) | 是 | Created by |
| `updated_by` | VARCHAR(128) | 是 | 最后更新者用户名 |
| `date_created` | DATETIME(6) | 是 | Created by |
| `date_updated` | DATETIME(6) | 否 | Created by |
| `comment` | LONGTEXT | 否 | Created by |
| `org_id` | VARCHAR(36) | 否 | 所属组织 ID，用于多租户数据隔离 |
| `id` | CHAR(32) | 否 | Full value |
| `key` | VARCHAR(64) | 否 | Full value |
| `value` | VARCHAR(128) | 否 | Full value |
| `full_value` | VARCHAR(4096) | 否 | Full value |
| `child_mark` | INT | 否 | - |
| `date_create` | DATETIME(6) | 否 | Create时间 |
| `parent_key` | VARCHAR(64) | 否 | - |
| `assets_amount` | INT | 否 | - |

**索引：**

- PRIMARY KEY: id
- UNIQUE `key`: key
- INDEX `key`: key
- INDEX `assets_node_org_id_400c35cb`: org_id
- INDEX `assets_node_parent_key_1d05e1aa`: parent_key

---

### `assets_pingautomation`

**资产连通性检测自动化任务**

| 字段 | 类型 | 可空 | 说明 |
| --- | --- | --- | --- |
| `baseautomation_ptr_id` | CHAR(32) | 否 | baseautomation_ptr 的关联 ID |

**索引：**

- PRIMARY KEY: baseautomation_ptr_id
- FK `assets_pingautomatio_baseautomation_ptr_i_175d6fb0_fk_assets_ba`: baseautomation_ptr_id → `assets_baseautomation`.id

---

### `assets_platform`

**资产平台（操作系统/设备类型定义）**

| 字段 | 类型 | 可空 | 说明 |
| --- | --- | --- | --- |
| `id` | INT | 否 | Full value |
| `created_by` | VARCHAR(128) | 是 | Created by |
| `updated_by` | VARCHAR(128) | 是 | 最后更新者用户名 |
| `date_created` | DATETIME(6) | 是 | Created by |
| `date_updated` | DATETIME(6) | 否 | Created by |
| `comment` | LONGTEXT | 否 | Created by |
| `name` | VARCHAR(50) | 否 | Name |
| `category` | VARCHAR(32) | 否 | - |
| `type` | VARCHAR(32) | 否 | Last execution date |
| `meta` | LONGTEXT | 是 | 元数据 |
| `internal` | BOOLEAN | 否 | - |
| `charset` | VARCHAR(8) | 否 | - |
| `gateway_enabled` | BOOLEAN | 否 | - |
| `su_enabled` | BOOLEAN | 否 | - |
| `su_method` | VARCHAR(32) | 是 | - |
| `custom_fields` | LONGTEXT | 是 | - |
| `ds_enabled` | BOOLEAN | 否 | - |

**索引：**

- PRIMARY KEY: id
- UNIQUE `name`: name
- INDEX `name`: name

---

### `assets_platformautomation`

**平台自动化配置**

| 字段 | 类型 | 可空 | 说明 |
| --- | --- | --- | --- |
| `id` | INT | 否 | Full value |
| `ansible_enabled` | BOOLEAN | 否 | - |
| `ansible_config` | LONGTEXT | 否 | - |
| `ping_enabled` | BOOLEAN | 否 | - |
| `ping_method` | VARCHAR(32) | 是 | - |
| `ping_params` | LONGTEXT | 否 | - |
| `gather_facts_enabled` | BOOLEAN | 否 | - |
| `gather_facts_method` | LONGTEXT | 是 | - |
| `gather_facts_params` | LONGTEXT | 否 | - |
| `change_secret_enabled` | BOOLEAN | 否 | - |
| `change_secret_method` | LONGTEXT | 是 | - |
| `change_secret_params` | LONGTEXT | 否 | - |
| `push_account_enabled` | BOOLEAN | 否 | - |
| `push_account_method` | LONGTEXT | 是 | - |
| `push_account_params` | LONGTEXT | 否 | - |
| `verify_account_enabled` | BOOLEAN | 否 | - |
| `verify_account_method` | LONGTEXT | 是 | - |
| `verify_account_params` | LONGTEXT | 否 | - |
| `gather_accounts_enabled` | BOOLEAN | 否 | - |
| `gather_accounts_method` | LONGTEXT | 是 | - |
| `gather_accounts_params` | LONGTEXT | 否 | - |
| `remove_account_enabled` | BOOLEAN | 否 | - |
| `remove_account_method` | LONGTEXT | 是 | - |
| `remove_account_params` | LONGTEXT | 否 | - |
| `platform_id` | INT | 是 | platform 的关联 ID |

**索引：**

- PRIMARY KEY: id
- UNIQUE `platform_id`: platform_id
- INDEX `platform_id`: platform_id
- FK `assets_platformautom_platform_id_032a082f_fk_assets_pl`: platform_id → `assets_platform`.id

---

### `assets_platformprotocol`

**平台支持的协议配置**

| 字段 | 类型 | 可空 | 说明 |
| --- | --- | --- | --- |
| `id` | INT | 否 | Full value |
| `name` | VARCHAR(32) | 否 | Name |
| `port` | INT | 否 | Port |
| `primary` | BOOLEAN | 否 | Primary |
| `required` | BOOLEAN | 否 | Required |
| `default` | BOOLEAN | 否 | Default |
| `public` | BOOLEAN | 否 | Public |
| `setting` | LONGTEXT | 否 | Setting |
| `platform_id` | INT | 否 | platform 的关联 ID |

**索引：**

- PRIMARY KEY: id
- INDEX `assets_platformproto_platform_id_b77e3926_fk_assets_pl`: platform_id
- FK `assets_platformproto_platform_id_b77e3926_fk_assets_pl`: platform_id → `assets_platform`.id

---

### `assets_protocol`

**协议定义（SSH/RDP/VNC/Telnet 等）**

| 字段 | 类型 | 可空 | 说明 |
| --- | --- | --- | --- |
| `id` | INT | 否 | Full value |
| `name` | VARCHAR(32) | 否 | Name |
| `port` | INT | 否 | Port |
| `asset_id` | CHAR(32) | 否 | 关联资产 ID |

**索引：**

- PRIMARY KEY: id
- INDEX `assets_protocol_asset_id_e66dbaeb_fk_assets_asset_id`: asset_id
- FK `assets_protocol_asset_id_e66dbaeb_fk_assets_asset_id`: asset_id → `assets_asset`.id

---

### `assets_web`

**Web 资产（URL/应用）**

| 字段 | 类型 | 可空 | 说明 |
| --- | --- | --- | --- |
| `asset_ptr_id` | CHAR(32) | 否 | asset_ptr 的关联 ID |
| `autofill` | VARCHAR(16) | 否 | - |
| `username_selector` | VARCHAR(128) | 否 | - |
| `password_selector` | VARCHAR(128) | 否 | - |
| `submit_selector` | VARCHAR(128) | 否 | - |
| `script` | LONGTEXT | 否 | - |

**索引：**

- PRIMARY KEY: asset_ptr_id
- FK `assets_web_asset_ptr_id_c7c00478_fk_assets_asset_id`: asset_ptr_id → `assets_asset`.id

---

### `assets_zone`

**区域/域配置（网络隔离区域）**

| 字段 | 类型 | 可空 | 说明 |
| --- | --- | --- | --- |
| `created_by` | VARCHAR(128) | 是 | Created by |
| `updated_by` | VARCHAR(128) | 是 | 最后更新者用户名 |
| `date_created` | DATETIME(6) | 是 | Created by |
| `date_updated` | DATETIME(6) | 否 | Created by |
| `comment` | LONGTEXT | 否 | Created by |
| `id` | CHAR(32) | 否 | Full value |
| `org_id` | VARCHAR(36) | 否 | 所属组织 ID，用于多租户数据隔离 |
| `name` | VARCHAR(128) | 否 | Name |

**索引：**

- PRIMARY KEY: id
- UNIQUE `assets_domain_org_id_name_f058d44e_uniq`: org_id,name
- INDEX `assets_domain_org_id_name_f058d44e_uniq`: org_id,name
- INDEX `assets_domain_org_id_50f4640b`: org_id

---

## 审计日志（Audits）

记录用户登录、操作、FTP、密码变更等审计日志

### `audits_activitylog`

**用户活动日志**

| 字段 | 类型 | 可空 | 说明 |
| --- | --- | --- | --- |
| `org_id` | VARCHAR(36) | 否 | 所属组织 ID，用于多租户数据隔离 |
| `id` | CHAR(32) | 否 | Datetime |
| `type` | VARCHAR(2) | 是 | Login date |
| `resource_id` | VARCHAR(36) | 否 | Datetime |
| `datetime` | DATETIME(6) | 否 | Datetime |
| `detail` | LONGTEXT | 否 | Detail |
| `detail_id` | VARCHAR(36) | 是 | Detail ID |

**索引：**

- PRIMARY KEY: id
- INDEX `audits_activitylog_org_id_64d1c757`: org_id
- INDEX `audits_activitylog_resource_id_c800d06d`: resource_id
- INDEX `audits_activitylog_datetime_e5189044`: datetime

---

### `audits_ftplog`

**FTP 操作日志**

| 字段 | 类型 | 可空 | 说明 |
| --- | --- | --- | --- |
| `org_id` | VARCHAR(36) | 否 | 所属组织 ID，用于多租户数据隔离 |
| `id` | CHAR(32) | 否 | Datetime |
| `user` | VARCHAR(128) | 否 | User |
| `remote_addr` | VARCHAR(128) | 是 | Datetime |
| `asset` | VARCHAR(768) | 否 | 资产 |
| `account` | VARCHAR(128) | 否 | 账户 |
| `operate` | VARCHAR(16) | 否 | - |
| `filename` | VARCHAR(1024) | 否 | - |
| `is_success` | BOOLEAN | 否 | 是否成功 |
| `date_start` | DATETIME(6) | 否 | 开始时间 |
| `has_file` | BOOLEAN | 否 | 是否有文件操作记录 |
| `session` | VARCHAR(36) | 否 | 会话 |

**索引：**

- PRIMARY KEY: id
- INDEX `audits_ftplog_org_id_de02081f`: org_id
- INDEX `audits_ftplog_account_5b6c1128`: account
- INDEX `audits_ftplog_asset_96353a5a`: asset
- INDEX `idx_date_start_org`: date_start,org_id

---

### `audits_integrationapplicationlog`

**集成应用操作日志**

| 字段 | 类型 | 可空 | 说明 |
| --- | --- | --- | --- |
| `id` | CHAR(32) | 否 | Datetime |
| `remote_addr` | CHAR(39) | 否 | Datetime |
| `service` | VARCHAR(128) | 否 | - |
| `service_id` | CHAR(32) | 否 | service 的关联 ID |
| `asset` | VARCHAR(128) | 否 | 资产 |
| `account` | VARCHAR(128) | 否 | 账户 |
| `datetime` | DATETIME(6) | 否 | Datetime |

**索引：**

- PRIMARY KEY: id

---

### `audits_operatelog`

**运维操作日志**

| 字段 | 类型 | 可空 | 说明 |
| --- | --- | --- | --- |
| `org_id` | VARCHAR(36) | 否 | 所属组织 ID，用于多租户数据隔离 |
| `id` | CHAR(32) | 否 | Datetime |
| `user` | VARCHAR(128) | 否 | User |
| `action` | VARCHAR(16) | 否 | 操作类型 |
| `resource_type` | VARCHAR(64) | 否 | Datetime |
| `resource` | VARCHAR(128) | 否 | Datetime |
| `resource_id` | VARCHAR(128) | 否 | Datetime |
| `remote_addr` | VARCHAR(128) | 是 | Datetime |
| `datetime` | DATETIME(6) | 否 | Datetime |
| `diff` | LONGTEXT | 是 | - |

**索引：**

- PRIMARY KEY: id
- INDEX `audits_operatelog_org_id_2ee40268`: org_id
- INDEX `audits_operatelog_resource_id_64e409c0`: resource_id
- INDEX `audits_operatelog_datetime_360b2242`: datetime

---

### `audits_passwordchangelog`

**密码变更日志**

| 字段 | 类型 | 可空 | 说明 |
| --- | --- | --- | --- |
| `id` | CHAR(32) | 否 | Datetime |
| `user` | VARCHAR(128) | 否 | User |
| `change_by` | VARCHAR(128) | 否 | - |
| `remote_addr` | VARCHAR(128) | 是 | Datetime |
| `datetime` | DATETIME(6) | 否 | Datetime |

**索引：**

- PRIMARY KEY: id
- INDEX `audits_passwordchangelog_datetime_6bbd9195`: datetime

---

### `audits_userloginlog`

**用户登录日志**

| 字段 | 类型 | 可空 | 说明 |
| --- | --- | --- | --- |
| `id` | CHAR(32) | 否 | Datetime |
| `username` | VARCHAR(128) | 否 | 用户名 |
| `type` | VARCHAR(2) | 否 | Login date |
| `ip` | CHAR(39) | 否 | IP 地址 |
| `city` | VARCHAR(254) | 是 | Login date |
| `user_agent` | VARCHAR(254) | 是 | Login date |
| `mfa` | SMALLINT | 否 | - |
| `reason` | VARCHAR(128) | 否 | - |
| `status` | BOOLEAN | 否 | 状态 |
| `datetime` | DATETIME(6) | 否 | Datetime |
| `backend` | VARCHAR(32) | 否 | Login date |
| `reason_code` | VARCHAR(64) | 否 | - |
| `reason_params` | LONGTEXT | 否 | - |

**索引：**

- PRIMARY KEY: id
- INDEX `audits_userloginlog_datetime_165fc15a`: datetime

---

### `audits_usersession`

**用户会话记录**

| 字段 | 类型 | 可空 | 说明 |
| --- | --- | --- | --- |
| `id` | CHAR(32) | 否 | Datetime |
| `ip` | CHAR(39) | 否 | IP 地址 |
| `key` | VARCHAR(128) | 否 | 键 |
| `city` | VARCHAR(254) | 是 | Login date |
| `user_agent` | VARCHAR(254) | 是 | Login date |
| `type` | VARCHAR(2) | 否 | Login date |
| `backend` | VARCHAR(32) | 否 | Login date |
| `date_created` | DATETIME(6) | 是 | Login date |
| `user_id` | CHAR(32) | 否 | 用户 ID |

**索引：**

- PRIMARY KEY: id
- INDEX `audits_usersession_user_id_38846be8_fk_users_user_id`: user_id
- FK `audits_usersession_user_id_38846be8_fk_users_user_id`: user_id → `users_user`.id

---

## Django 认证（Auth）

Django 内置认证系统，用户组和权限

### `auth_group`

**Django 认证用户组**

| 字段 | 类型 | 可空 | 说明 |
| --- | --- | --- | --- |
| `id` | INT | 否 | 主键，UUID 格式（无连字符，32 位） |
| `name` | VARCHAR(150) | 否 | 名称 |

**索引：**

- PRIMARY KEY: id
- UNIQUE `name`: name
- INDEX `name`: name

---

### `auth_group_permissions`

**用户组与权限的多对多关联**

| 字段 | 类型 | 可空 | 说明 |
| --- | --- | --- | --- |
| `id` | INT | 否 | 主键，UUID 格式（无连字符，32 位） |
| `group_id` | INT | 否 | group 的关联 ID |
| `permission_id` | INT | 否 | permission 的关联 ID |

**索引：**

- PRIMARY KEY: id
- UNIQUE `auth_group_permissions_group_id_permission_id_0cd325b0_uniq`: group_id,permission_id
- INDEX `auth_group_permissions_group_id_permission_id_0cd325b0_uniq`: group_id,permission_id
- INDEX `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm`: permission_id
- FK `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm`: permission_id → `auth_permission`.id
- FK `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id`: group_id → `auth_group`.id

---

### `auth_permission`

**Django 权限定义**

| 字段 | 类型 | 可空 | 说明 |
| --- | --- | --- | --- |
| `id` | INT | 否 | 主键，UUID 格式（无连字符，32 位） |
| `name` | VARCHAR(255) | 否 | 名称 |
| `content_type_id` | INT | 否 | content_type 的关联 ID |
| `codename` | VARCHAR(100) | 否 | - |

**索引：**

- PRIMARY KEY: id
- UNIQUE `auth_permission_content_type_id_codename_01ab375a_uniq`: content_type_id,codename
- INDEX `auth_permission_content_type_id_codename_01ab375a_uniq`: content_type_id,codename
- FK `auth_permission_content_type_id_2f476e4b_fk_django_co`: content_type_id → `django_content_type`.id

---

## 认证令牌（Authentication）

管理连接令牌、访问密钥、SSH 密钥、Passkey 等认证凭证

### `authentication_accesskey`

**API 访问密钥**

| 字段 | 类型 | 可空 | 说明 |
| --- | --- | --- | --- |
| `id` | CHAR(32) | 否 | IP group |
| `secret` | LONGTEXT | 否 | 密钥/密码 |
| `ip_group` | LONGTEXT | 否 | IP group |
| `is_active` | BOOLEAN | 否 | Type |
| `date_last_used` | DATETIME(6) | 是 | Date last used |
| `date_created` | DATETIME(6) | 否 | 创建时间 |
| `user_id` | CHAR(32) | 否 | 用户 ID |

**索引：**

- PRIMARY KEY: id
- INDEX `authentication_accesskey_user_id_3636c132_fk_users_user_id`: user_id
- FK `authentication_accesskey_user_id_3636c132_fk_users_user_id`: user_id → `users_user`.id

---

### `authentication_connectiontoken`

**连接令牌（资产/应用连接凭证）**

| 字段 | 类型 | 可空 | 说明 |
| --- | --- | --- | --- |
| `created_by` | VARCHAR(128) | 是 | 创建者用户名 |
| `updated_by` | VARCHAR(128) | 是 | 最后更新者用户名 |
| `date_created` | DATETIME(6) | 是 | 创建时间 |
| `date_updated` | DATETIME(6) | 否 | 更新时间 |
| `comment` | LONGTEXT | 否 | 备注 |
| `id` | CHAR(32) | 否 | IP group |
| `org_id` | VARCHAR(36) | 否 | 所属组织 ID，用于多租户数据隔离 |
| `value` | VARCHAR(64) | 否 | User |
| `account` | VARCHAR(128) | 否 | 账户 |
| `input_username` | VARCHAR(128) | 否 | - |
| `input_secret` | LONGTEXT | 否 | - |
| `protocol` | VARCHAR(16) | 否 | 协议（ssh/rdp/vnc/telnet） |
| `connect_method` | VARCHAR(32) | 否 | - |
| `connect_options` | LONGTEXT | 否 | - |
| `user_display` | VARCHAR(128) | 否 | 用户显示 |
| `asset_display` | VARCHAR(128) | 否 | From ticket |
| `is_reusable` | BOOLEAN | 否 | From ticket |
| `date_expired` | DATETIME(6) | 否 | From ticket |
| `is_active` | BOOLEAN | 否 | Type |
| `asset_id` | CHAR(32) | 是 | 关联资产 ID |
| `from_ticket_id` | CHAR(32) | 是 | from_ticket 的关联 ID |
| `user_id` | CHAR(32) | 是 | 用户 ID |
| `face_monitor_token` | VARCHAR(128) | 是 | Type |
| `type` | VARCHAR(16) | 否 | Type |
| `remote_addr` | VARCHAR(128) | 是 | Type |
| `input_secret_type` | VARCHAR(16) | 是 | - |

**索引：**

- PRIMARY KEY: id
- UNIQUE `from_ticket_id`: from_ticket_id
- INDEX `from_ticket_id`: from_ticket_id
- INDEX `authentication_connectiontoken_org_id_ad630aa2`: org_id
- INDEX `authentication_conne_asset_id_8dad7e84_fk_assets_as`: asset_id
- INDEX `authentication_connectiontoken_user_id_08533d74_fk_users_user_id`: user_id
- FK `authentication_conne_asset_id_8dad7e84_fk_assets_as`: asset_id → `assets_asset`.id
- FK `authentication_conne_from_ticket_id_10462d91_fk_tickets_a`: from_ticket_id → `tickets_applyloginassetticket`.ticket_ptr_id
- FK `authentication_connectiontoken_user_id_08533d74_fk_users_user_id`: user_id → `users_user`.id

---

### `authentication_passkey`

**Passkey/FIDO2 认证密钥**

| 字段 | 类型 | 可空 | 说明 |
| --- | --- | --- | --- |
| `created_by` | VARCHAR(128) | 是 | 创建者用户名 |
| `updated_by` | VARCHAR(128) | 是 | 最后更新者用户名 |
| `date_created` | DATETIME(6) | 是 | 创建时间 |
| `date_updated` | DATETIME(6) | 否 | 更新时间 |
| `comment` | LONGTEXT | 否 | 备注 |
| `id` | CHAR(32) | 否 | IP group |
| `name` | VARCHAR(255) | 否 | Active |
| `is_active` | BOOLEAN | 否 | Type |
| `platform` | VARCHAR(255) | 否 | 平台（操作系统/设备类型） |
| `added_on` | DATETIME(6) | 否 | - |
| `date_last_used` | DATETIME(6) | 是 | Date last used |
| `credential_id` | VARCHAR(255) | 否 | credential 的关联 ID |
| `token` | VARCHAR(1024) | 否 | 令牌 |
| `user_id` | CHAR(32) | 否 | 用户 ID |

**索引：**

- PRIMARY KEY: id
- UNIQUE `credential_id`: credential_id
- INDEX `credential_id`: credential_id
- INDEX `authentication_passkey_user_id_eea4b831_fk_users_user_id`: user_id
- FK `authentication_passkey_user_id_eea4b831_fk_users_user_id`: user_id → `users_user`.id

---

### `authentication_privatetoken`

**私有令牌（用户个人 API 令牌）**

| 字段 | 类型 | 可空 | 说明 |
| --- | --- | --- | --- |
| `key` | VARCHAR(40) | 否 | 键 |
| `created` | DATETIME(6) | 否 | - |
| `date_last_used` | DATETIME(6) | 是 | Date last used |
| `user_id` | CHAR(32) | 否 | 用户 ID |

**索引：**

- PRIMARY KEY: key
- UNIQUE `user_id`: user_id
- INDEX `user_id`: user_id
- FK `authentication_privatetoken_user_id_2dd25d96_fk_users_user_id`: user_id → `users_user`.id

---

### `authentication_sshkey`

**SSH 公钥**

| 字段 | 类型 | 可空 | 说明 |
| --- | --- | --- | --- |
| `created_by` | VARCHAR(128) | 是 | 创建者用户名 |
| `updated_by` | VARCHAR(128) | 是 | 最后更新者用户名 |
| `date_created` | DATETIME(6) | 是 | 创建时间 |
| `date_updated` | DATETIME(6) | 否 | 更新时间 |
| `comment` | LONGTEXT | 否 | 备注 |
| `id` | CHAR(32) | 否 | IP group |
| `name` | VARCHAR(128) | 否 | Active |
| `is_active` | BOOLEAN | 否 | Type |
| `private_key` | LONGTEXT | 是 | 私钥 |
| `public_key` | LONGTEXT | 是 | 公钥 |
| `date_last_used` | DATETIME(6) | 是 | Date last used |
| `user_id` | CHAR(32) | 否 | 用户 ID |

**索引：**

- PRIMARY KEY: id
- INDEX `authentication_sshkey_user_id_a1d5dad1`: user_id

---

### `authentication_ssotoken`

**SSO 登录令牌**

| 字段 | 类型 | 可空 | 说明 |
| --- | --- | --- | --- |
| `created_by` | VARCHAR(128) | 是 | 创建者用户名 |
| `updated_by` | VARCHAR(128) | 是 | 最后更新者用户名 |
| `date_created` | DATETIME(6) | 是 | 创建时间 |
| `date_updated` | DATETIME(6) | 否 | 更新时间 |
| `comment` | LONGTEXT | 否 | 备注 |
| `authkey` | CHAR(32) | 否 | Token |
| `expired` | BOOLEAN | 否 | Expired |
| `user_id` | CHAR(32) | 否 | 用户 ID |

**索引：**

- PRIMARY KEY: authkey
- INDEX `authentication_ssotoken_user_id_eda7c917`: user_id

---

### `authentication_temptoken`

**临时令牌（一次性使用）**

| 字段 | 类型 | 可空 | 说明 |
| --- | --- | --- | --- |
| `created_by` | VARCHAR(128) | 是 | 创建者用户名 |
| `updated_by` | VARCHAR(128) | 是 | 最后更新者用户名 |
| `date_created` | DATETIME(6) | 是 | 创建时间 |
| `date_updated` | DATETIME(6) | 否 | 更新时间 |
| `comment` | LONGTEXT | 否 | 备注 |
| `id` | CHAR(32) | 否 | IP group |
| `username` | VARCHAR(128) | 否 | 用户名 |
| `secret` | LONGTEXT | 否 | 密钥/密码 |
| `verified` | BOOLEAN | 否 | - |
| `date_verified` | DATETIME(6) | 是 | 最后验证时间 |
| `date_expired` | DATETIME(6) | 否 | From ticket |

**索引：**

- PRIMARY KEY: id

---

## 验证码（Captcha）

验证码存储

### `captcha_captchastore`

**验证码存储**

| 字段 | 类型 | 可空 | 说明 |
| --- | --- | --- | --- |
| `id` | INT | 否 | 主键，UUID 格式（无连字符，32 位） |
| `challenge` | VARCHAR(32) | 否 | - |
| `response` | VARCHAR(32) | 否 | - |
| `hashkey` | VARCHAR(40) | 否 | - |
| `expiration` | DATETIME(6) | 否 | - |

**索引：**

- PRIMARY KEY: id
- UNIQUE `hashkey`: hashkey
- INDEX `hashkey`: hashkey

---

## Django 框架（Django）

Django 框架内部表，包括会话、迁移、Celery 任务调度等

### `django_admin_log`

**Django 后台管理操作日志**

| 字段 | 类型 | 可空 | 说明 |
| --- | --- | --- | --- |
| `id` | INT | 否 | 主键，UUID 格式（无连字符，32 位） |
| `action_time` | DATETIME(6) | 否 | - |
| `object_id` | LONGTEXT | 是 | object 的关联 ID |
| `object_repr` | VARCHAR(200) | 否 | - |
| `action_flag` | SMALLINT(5) UNSIGNED | 否 | - |
| `change_message` | LONGTEXT | 否 | - |
| `content_type_id` | INT | 是 | content_type 的关联 ID |
| `user_id` | CHAR(32) | 否 | 用户 ID |

**索引：**

- PRIMARY KEY: id
- INDEX `django_admin_log_content_type_id_c4bce8eb_fk_django_co`: content_type_id
- INDEX `django_admin_log_user_id_c564eba6_fk_users_user_id`: user_id
- FK `django_admin_log_content_type_id_c4bce8eb_fk_django_co`: content_type_id → `django_content_type`.id
- FK `django_admin_log_user_id_c564eba6_fk_users_user_id`: user_id → `users_user`.id

---

### `django_cas_ng_proxygrantingticket`

**CAS 代理授权票据**

| 字段 | 类型 | 可空 | 说明 |
| --- | --- | --- | --- |
| `id` | INT | 否 | 主键，UUID 格式（无连字符，32 位） |
| `session_key` | VARCHAR(736) | 是 | 会话密钥 |
| `pgtiou` | VARCHAR(255) | 是 | - |
| `pgt` | VARCHAR(255) | 是 | - |
| `date` | DATETIME(6) | 否 | - |
| `user_id` | CHAR(32) | 是 | 用户 ID |

**索引：**

- PRIMARY KEY: id
- UNIQUE `django_cas_ng_proxygrant_session_key_user_id_4cd2ea19_uniq`: session_key,user_id
- INDEX `django_cas_ng_proxygrant_session_key_user_id_4cd2ea19_uniq`: session_key,user_id
- INDEX `django_cas_ng_proxyg_user_id_f833edd2_fk_users_use`: user_id
- FK `django_cas_ng_proxyg_user_id_f833edd2_fk_users_use`: user_id → `users_user`.id

---

### `django_cas_ng_sessionticket`

**CAS 会话票据**

| 字段 | 类型 | 可空 | 说明 |
| --- | --- | --- | --- |
| `id` | INT | 否 | 主键，UUID 格式（无连字符，32 位） |
| `session_key` | VARCHAR(736) | 否 | 会话密钥 |
| `ticket` | VARCHAR(1024) | 否 | - |

**索引：**

- PRIMARY KEY: id

---

### `django_celery_beat_clockedschedule`

**Celery 定时任务-时钟调度（指定时间执行）**

| 字段 | 类型 | 可空 | 说明 |
| --- | --- | --- | --- |
| `id` | INT | 否 | 主键，UUID 格式（无连字符，32 位） |
| `clocked_time` | DATETIME(6) | 否 | - |

**索引：**

- PRIMARY KEY: id

---

### `django_celery_beat_crontabschedule`

**Celery 定时任务-Cron 调度（周期性执行）**

| 字段 | 类型 | 可空 | 说明 |
| --- | --- | --- | --- |
| `id` | INT | 否 | 主键，UUID 格式（无连字符，32 位） |
| `minute` | VARCHAR(240) | 否 | - |
| `hour` | VARCHAR(96) | 否 | - |
| `day_of_week` | VARCHAR(64) | 否 | - |
| `day_of_month` | VARCHAR(124) | 否 | - |
| `month_of_year` | VARCHAR(64) | 否 | - |
| `timezone` | VARCHAR(63) | 否 | - |

**索引：**

- PRIMARY KEY: id

---

### `django_celery_beat_intervalschedule`

**Celery 定时任务-间隔调度（固定间隔执行）**

| 字段 | 类型 | 可空 | 说明 |
| --- | --- | --- | --- |
| `id` | INT | 否 | 主键，UUID 格式（无连字符，32 位） |
| `every` | INT | 否 | - |
| `period` | VARCHAR(24) | 否 | - |

**索引：**

- PRIMARY KEY: id

---

### `django_celery_beat_periodictask`

**Celery 定时任务定义**

| 字段 | 类型 | 可空 | 说明 |
| --- | --- | --- | --- |
| `id` | INT | 否 | 主键，UUID 格式（无连字符，32 位） |
| `name` | VARCHAR(200) | 否 | 名称 |
| `task` | VARCHAR(200) | 否 | 任务 |
| `args` | LONGTEXT | 否 | 参数 |
| `kwargs` | LONGTEXT | 否 | 关键字参数 |
| `queue` | VARCHAR(200) | 是 | - |
| `exchange` | VARCHAR(200) | 是 | - |
| `routing_key` | VARCHAR(200) | 是 | - |
| `expires` | DATETIME(6) | 是 | 过期时间 |
| `enabled` | BOOLEAN | 否 | 是否启用 |
| `last_run_at` | DATETIME(6) | 是 | - |
| `total_run_count` | INT(10) UNSIGNED | 否 | - |
| `date_changed` | DATETIME(6) | 否 | Changed时间 |
| `description` | LONGTEXT | 否 | - |
| `crontab_id` | INT | 是 | crontab 的关联 ID |
| `interval_id` | INT | 是 | interval 的关联 ID |
| `solar_id` | INT | 是 | solar 的关联 ID |
| `one_off` | BOOLEAN | 否 | - |
| `start_time` | DATETIME(6) | 是 | - |
| `priority` | INT(10) UNSIGNED | 是 | 优先级 |
| `headers` | LONGTEXT | 否 | 请求头 |
| `clocked_id` | INT | 是 | clocked 的关联 ID |
| `expire_seconds` | INT(10) UNSIGNED | 是 | - |

**索引：**

- PRIMARY KEY: id
- UNIQUE `name`: name
- INDEX `name`: name
- INDEX `django_celery_beat_p_crontab_id_d3cba168_fk_django_ce`: crontab_id
- INDEX `django_celery_beat_p_interval_id_a8ca27da_fk_django_ce`: interval_id
- INDEX `django_celery_beat_p_solar_id_a87ce72c_fk_django_ce`: solar_id
- INDEX `django_celery_beat_p_clocked_id_47a69f82_fk_django_ce`: clocked_id
- FK `django_celery_beat_p_clocked_id_47a69f82_fk_django_ce`: clocked_id → `django_celery_beat_clockedschedule`.id
- FK `django_celery_beat_p_crontab_id_d3cba168_fk_django_ce`: crontab_id → `django_celery_beat_crontabschedule`.id
- FK `django_celery_beat_p_interval_id_a8ca27da_fk_django_ce`: interval_id → `django_celery_beat_intervalschedule`.id
- FK `django_celery_beat_p_solar_id_a87ce72c_fk_django_ce`: solar_id → `django_celery_beat_solarschedule`.id

---

### `django_celery_beat_periodictasks`

**Celery 定时任务映射（多对多）**

| 字段 | 类型 | 可空 | 说明 |
| --- | --- | --- | --- |
| `ident` | SMALLINT | 否 | - |
| `last_update` | DATETIME(6) | 否 | - |

**索引：**

- PRIMARY KEY: ident

---

### `django_celery_beat_solarschedule`

**Celery 定时任务-日出日落调度**

| 字段 | 类型 | 可空 | 说明 |
| --- | --- | --- | --- |
| `id` | INT | 否 | 主键，UUID 格式（无连字符，32 位） |
| `event` | VARCHAR(24) | 否 | - |

**索引：**

- PRIMARY KEY: id
- UNIQUE `django_celery_beat_solar_event_latitude_longitude_ba64999a_uniq`: event,latitude,longitude
- INDEX `django_celery_beat_solar_event_latitude_longitude_ba64999a_uniq`: event,latitude,longitude

---

### `django_content_type`

**Django 内容类型（模型注册表）**

| 字段 | 类型 | 可空 | 说明 |
| --- | --- | --- | --- |
| `id` | INT | 否 | 主键，UUID 格式（无连字符，32 位） |
| `app_label` | VARCHAR(100) | 否 | - |
| `model` | VARCHAR(100) | 否 | - |

**索引：**

- PRIMARY KEY: id
- UNIQUE `django_content_type_app_label_model_76bd3d3b_uniq`: app_label,model
- INDEX `django_content_type_app_label_model_76bd3d3b_uniq`: app_label,model

---

### `django_migrations`

**Django 数据库迁移记录**

| 字段 | 类型 | 可空 | 说明 |
| --- | --- | --- | --- |
| `id` | INT | 否 | 主键，UUID 格式（无连字符，32 位） |
| `app` | VARCHAR(255) | 否 | - |
| `name` | VARCHAR(255) | 否 | 名称 |
| `applied` | DATETIME(6) | 否 | - |

**索引：**

- PRIMARY KEY: id

---

### `django_session`

**Django 会话存储**

| 字段 | 类型 | 可空 | 说明 |
| --- | --- | --- | --- |
| `session_key` | VARCHAR(40) | 否 | 会话密钥 |
| `session_data` | LONGTEXT | 否 | - |
| `expire_date` | DATETIME(6) | 否 | - |

**索引：**

- PRIMARY KEY: session_key
- INDEX `django_session_expire_date_a5c62663`: expire_date

---

## 标签管理（Labels）

资源标签定义与关联

### `labels_label`

**标签定义**

| 字段 | 类型 | 可空 | 说明 |
| --- | --- | --- | --- |
| `created_by` | VARCHAR(128) | 是 | 创建者用户名 |
| `updated_by` | VARCHAR(128) | 是 | 最后更新者用户名 |
| `date_created` | DATETIME(6) | 是 | 创建时间 |
| `date_updated` | DATETIME(6) | 否 | 更新时间 |
| `comment` | LONGTEXT | 否 | 备注 |
| `id` | CHAR(32) | 否 | 主键，UUID 格式（无连字符，32 位） |
| `org_id` | VARCHAR(36) | 否 | 所属组织 ID，用于多租户数据隔离 |
| `name` | VARCHAR(64) | 否 | 名称 |
| `value` | VARCHAR(64) | 否 | 值 |
| `internal` | BOOLEAN | 否 | - |
| `color` | VARCHAR(32) | 否 | - |

**索引：**

- PRIMARY KEY: id
- UNIQUE `labels_label_name_value_org_id_6919f24e_uniq`: name,value,org_id
- INDEX `labels_label_name_value_org_id_6919f24e_uniq`: name,value,org_id
- INDEX `labels_label_org_id_b6b7e424`: org_id
- INDEX `labels_label_name_c462fba5`: name

---

### `labels_labeledresource`

**资源与标签的多对多关联**

| 字段 | 类型 | 可空 | 说明 |
| --- | --- | --- | --- |
| `created_by` | VARCHAR(128) | 是 | 创建者用户名 |
| `updated_by` | VARCHAR(128) | 是 | 最后更新者用户名 |
| `date_created` | DATETIME(6) | 是 | 创建时间 |
| `date_updated` | DATETIME(6) | 否 | 更新时间 |
| `comment` | LONGTEXT | 否 | 备注 |
| `id` | CHAR(32) | 否 | 主键，UUID 格式（无连字符，32 位） |
| `org_id` | VARCHAR(36) | 否 | 所属组织 ID，用于多租户数据隔离 |
| `res_id` | VARCHAR(36) | 否 | res 的关联 ID |
| `label_id` | CHAR(32) | 否 | label 的关联 ID |
| `res_type_id` | INT | 否 | res_type 的关联 ID |

**索引：**

- PRIMARY KEY: id
- UNIQUE `labels_labeledresource_label_id_res_type_id_res_830349ab_uniq`: label_id,res_type_id,res_id,org_id
- INDEX `labels_labeledresource_label_id_res_type_id_res_830349ab_uniq`: label_id,res_type_id,res_id,org_id
- INDEX `labels_labeledresour_res_type_id_770d03bb_fk_django_co`: res_type_id
- INDEX `labels_labeledresource_org_id_d0fb1acc`: org_id
- INDEX `labels_labeledresource_res_id_0e341a87`: res_id
- FK `labels_labeledresour_res_type_id_770d03bb_fk_django_co`: res_type_id → `django_content_type`.id
- FK `labels_labeledresource_label_id_f37cf385_fk_labels_label_id`: label_id → `labels_label`.id

---

## 通知消息（Notifications）

站内信、系统消息订阅、通知模板等

### `notifications_messagecontent`

**通知消息内容模板**

| 字段 | 类型 | 可空 | 说明 |
| --- | --- | --- | --- |
| `created_by` | VARCHAR(128) | 是 | 创建者用户名 |
| `updated_by` | VARCHAR(128) | 是 | 最后更新者用户名 |
| `date_created` | DATETIME(6) | 是 | 创建时间 |
| `date_updated` | DATETIME(6) | 否 | 更新时间 |
| `id` | CHAR(32) | 否 | 主键，UUID 格式（无连字符，32 位） |
| `subject` | VARCHAR(1024) | 否 | 通知主题 |
| `message` | LONGTEXT | 否 | - |
| `is_broadcast` | BOOLEAN | 否 | Broadcast标记 |
| `sender_id` | CHAR(32) | 是 | sender 的关联 ID |
| `display_mode` | VARCHAR(32) | 否 | - |

**索引：**

- PRIMARY KEY: id
- INDEX `notifications_messagecontent_sender_id_1fabbbc5`: sender_id

---

### `notifications_messagecontent_groups`

**通知消息与用户组的关联**

| 字段 | 类型 | 可空 | 说明 |
| --- | --- | --- | --- |
| `id` | INT | 否 | 主键，UUID 格式（无连字符，32 位） |
| `messagecontent_id` | CHAR(32) | 否 | messagecontent 的关联 ID |
| `usergroup_id` | CHAR(32) | 否 | usergroup 的关联 ID |

**索引：**

- PRIMARY KEY: id
- UNIQUE `notifications_messagecon_messagecontent_id_usergr_5601acac_uniq`: messagecontent_id,usergroup_id
- INDEX `notifications_messagecon_messagecontent_id_usergr_5601acac_uniq`: messagecontent_id,usergroup_id
- INDEX `notifications_messag_usergroup_id_e9c9f9bb_fk_users_use`: usergroup_id
- FK `notifications_messag_messagecontent_id_20f26938_fk_notificat`: messagecontent_id → `notifications_messagecontent`.id
- FK `notifications_messag_usergroup_id_e9c9f9bb_fk_users_use`: usergroup_id → `users_usergroup`.id

---

### `notifications_sitemessage`

**站内信消息**

| 字段 | 类型 | 可空 | 说明 |
| --- | --- | --- | --- |
| `created_by` | VARCHAR(128) | 是 | 创建者用户名 |
| `updated_by` | VARCHAR(128) | 是 | 最后更新者用户名 |
| `date_created` | DATETIME(6) | 是 | 创建时间 |
| `date_updated` | DATETIME(6) | 否 | 更新时间 |
| `id` | CHAR(32) | 否 | 主键，UUID 格式（无连字符，32 位） |
| `has_read` | BOOLEAN | 否 | 是否Read |
| `read_at` | DATETIME(6) | 是 | - |
| `content_id` | CHAR(32) | 否 | content 的关联 ID |
| `user_id` | CHAR(32) | 否 | 用户 ID |

**索引：**

- PRIMARY KEY: id
- INDEX `notifications_sitemessage_content_id_d88b1594`: content_id
- INDEX `notifications_sitemessage_user_id_cde4e86b`: user_id

---

### `notifications_systemmsgsubscription`

**系统消息订阅配置**

| 字段 | 类型 | 可空 | 说明 |
| --- | --- | --- | --- |
| `created_by` | VARCHAR(128) | 是 | 创建者用户名 |
| `updated_by` | VARCHAR(128) | 是 | 最后更新者用户名 |
| `date_created` | DATETIME(6) | 是 | 创建时间 |
| `date_updated` | DATETIME(6) | 否 | 更新时间 |
| `id` | CHAR(32) | 否 | 主键，UUID 格式（无连字符，32 位） |
| `message_type` | VARCHAR(128) | 否 | System message |
| `receive_backends` | LONGTEXT | 否 | System message |

**索引：**

- PRIMARY KEY: id
- UNIQUE `message_type`: message_type
- INDEX `message_type`: message_type

---

### `notifications_systemmsgsubscription_groups`

**系统消息订阅与用户组的关联**

| 字段 | 类型 | 可空 | 说明 |
| --- | --- | --- | --- |
| `id` | INT | 否 | 主键，UUID 格式（无连字符，32 位） |
| `systemmsgsubscription_id` | CHAR(32) | 否 | systemmsgsubscription 的关联 ID |
| `usergroup_id` | CHAR(32) | 否 | usergroup 的关联 ID |

**索引：**

- PRIMARY KEY: id
- UNIQUE `notifications_systemmsgs_systemmsgsubscription_id_84119f33_uniq`: systemmsgsubscription_id,usergroup_id
- INDEX `notifications_systemmsgs_systemmsgsubscription_id_84119f33_uniq`: systemmsgsubscription_id,usergroup_id
- INDEX `notifications_system_usergroup_id_a1bedf56_fk_users_use`: usergroup_id
- FK `notifications_system_systemmsgsubscriptio_9c974da1_fk_notificat`: systemmsgsubscription_id → `notifications_systemmsgsubscription`.id
- FK `notifications_system_usergroup_id_a1bedf56_fk_users_use`: usergroup_id → `users_usergroup`.id

---

### `notifications_systemmsgsubscription_users`

**系统消息订阅与用户的关联**

| 字段 | 类型 | 可空 | 说明 |
| --- | --- | --- | --- |
| `id` | INT | 否 | 主键，UUID 格式（无连字符，32 位） |
| `systemmsgsubscription_id` | CHAR(32) | 否 | systemmsgsubscription 的关联 ID |
| `user_id` | CHAR(32) | 否 | 用户 ID |

**索引：**

- PRIMARY KEY: id
- UNIQUE `notifications_systemmsgs_systemmsgsubscription_id_b0446c97_uniq`: systemmsgsubscription_id,user_id
- INDEX `notifications_systemmsgs_systemmsgsubscription_id_b0446c97_uniq`: systemmsgsubscription_id,user_id
- INDEX `notifications_system_user_id_6a738c74_fk_users_use`: user_id
- FK `notifications_system_systemmsgsubscriptio_e26c38c8_fk_notificat`: systemmsgsubscription_id → `notifications_systemmsgsubscription`.id
- FK `notifications_system_user_id_6a738c74_fk_users_use`: user_id → `users_user`.id

---

### `notifications_usermsgsubscription`

**用户消息订阅**

| 字段 | 类型 | 可空 | 说明 |
| --- | --- | --- | --- |
| `created_by` | VARCHAR(128) | 是 | 创建者用户名 |
| `updated_by` | VARCHAR(128) | 是 | 最后更新者用户名 |
| `date_created` | DATETIME(6) | 是 | 创建时间 |
| `date_updated` | DATETIME(6) | 否 | 更新时间 |
| `id` | CHAR(32) | 否 | 主键，UUID 格式（无连字符，32 位） |
| `receive_backends` | LONGTEXT | 否 | System message |
| `user_id` | CHAR(32) | 否 | 用户 ID |

**索引：**

- PRIMARY KEY: id
- UNIQUE `user_id`: user_id
- INDEX `user_id`: user_id
- FK `notifications_userms_user_id_a8daa1ad_fk_users_use`: user_id → `users_user`.id

---

## OAuth2（OAuth2 Provider）

OAuth2 认证协议支持

### `oauth2_provider_accesstoken`

**OAuth2 访问令牌**

| 字段 | 类型 | 可空 | 说明 |
| --- | --- | --- | --- |
| `id` | BIGINT | 否 | 主键，UUID 格式（无连字符，32 位） |
| `token` | VARCHAR(255) | 否 | 令牌 |
| `expires` | DATETIME(6) | 否 | 过期时间 |
| `scope` | LONGTEXT | 否 | 作用域 |
| `application_id` | BIGINT | 是 | application 的关联 ID |
| `user_id` | CHAR(32) | 是 | 用户 ID |
| `created` | DATETIME(6) | 否 | - |
| `updated` | DATETIME(6) | 否 | - |
| `source_refresh_token_id` | BIGINT | 是 | source_refresh_token 的关联 ID |
| `id_token_id` | BIGINT | 是 | id_token 的关联 ID |

**索引：**

- PRIMARY KEY: id
- UNIQUE `token`: token
- UNIQUE `source_refresh_token_id`: source_refresh_token_id
- UNIQUE `id_token_id`: id_token_id
- INDEX `token`: token
- INDEX `source_refresh_token_id`: source_refresh_token_id
- INDEX `id_token_id`: id_token_id
- INDEX `oauth2_provider_acce_application_id_b22886e1_fk_oauth2_pr`: application_id
- INDEX `oauth2_provider_accesstoken_user_id_6e4c9a65_fk_users_user_id`: user_id
- FK `oauth2_provider_acce_application_id_b22886e1_fk_oauth2_pr`: application_id → `oauth2_provider_application`.id
- FK `oauth2_provider_acce_id_token_id_85db651b_fk_oauth2_pr`: id_token_id → `oauth2_provider_idtoken`.id
- FK `oauth2_provider_acce_source_refresh_token_e66fbc72_fk_oauth2_pr`: source_refresh_token_id → `oauth2_provider_refreshtoken`.id
- FK `oauth2_provider_accesstoken_user_id_6e4c9a65_fk_users_user_id`: user_id → `users_user`.id

---

### `oauth2_provider_application`

**OAuth2 应用注册**

| 字段 | 类型 | 可空 | 说明 |
| --- | --- | --- | --- |
| `id` | BIGINT | 否 | 主键，UUID 格式（无连字符，32 位） |
| `client_id` | VARCHAR(100) | 否 | 客户端 ID |
| `redirect_uris` | LONGTEXT | 否 | 重定向 URI |
| `client_type` | VARCHAR(32) | 否 | 客户端类型 |
| `authorization_grant_type` | VARCHAR(32) | 否 | 授权类型 |
| `client_secret` | VARCHAR(255) | 否 | 客户端密钥 |
| `name` | VARCHAR(255) | 否 | 名称 |
| `user_id` | CHAR(32) | 是 | 用户 ID |
| `skip_authorization` | BOOLEAN | 否 | 是否跳过授权确认 |
| `created` | DATETIME(6) | 否 | - |
| `updated` | DATETIME(6) | 否 | - |
| `algorithm` | VARCHAR(5) | 否 | - |
| `post_logout_redirect_uris` | LONGTEXT | 否 | - |
| `hash_client_secret` | BOOLEAN | 否 | - |
| `allowed_origins` | LONGTEXT | 否 | - |

**索引：**

- PRIMARY KEY: id
- UNIQUE `client_id`: client_id
- INDEX `client_id`: client_id
- INDEX `oauth2_provider_application_user_id_79829054_fk_users_user_id`: user_id
- INDEX `oauth2_provider_application_client_secret_53133678`: client_secret
- FK `oauth2_provider_application_user_id_79829054_fk_users_user_id`: user_id → `users_user`.id

---

### `oauth2_provider_grant`

**OAuth2 授权码**

| 字段 | 类型 | 可空 | 说明 |
| --- | --- | --- | --- |
| `id` | BIGINT | 否 | 主键，UUID 格式（无连字符，32 位） |
| `code` | VARCHAR(255) | 否 | - |
| `expires` | DATETIME(6) | 否 | 过期时间 |
| `redirect_uri` | LONGTEXT | 否 | - |
| `scope` | LONGTEXT | 否 | 作用域 |
| `application_id` | BIGINT | 否 | application 的关联 ID |
| `user_id` | CHAR(32) | 否 | 用户 ID |
| `created` | DATETIME(6) | 否 | - |
| `updated` | DATETIME(6) | 否 | - |
| `code_challenge` | VARCHAR(128) | 否 | - |
| `code_challenge_method` | VARCHAR(10) | 否 | - |
| `nonce` | VARCHAR(255) | 否 | - |
| `claims` | LONGTEXT | 否 | - |

**索引：**

- PRIMARY KEY: id
- UNIQUE `code`: code
- INDEX `code`: code
- INDEX `oauth2_provider_gran_application_id_81923564_fk_oauth2_pr`: application_id
- INDEX `oauth2_provider_grant_user_id_e8f62af8_fk_users_user_id`: user_id
- FK `oauth2_provider_gran_application_id_81923564_fk_oauth2_pr`: application_id → `oauth2_provider_application`.id
- FK `oauth2_provider_grant_user_id_e8f62af8_fk_users_user_id`: user_id → `users_user`.id

---

### `oauth2_provider_idtoken`

**OAuth2 ID 令牌**

| 字段 | 类型 | 可空 | 说明 |
| --- | --- | --- | --- |
| `id` | BIGINT | 否 | 主键，UUID 格式（无连字符，32 位） |
| `jti` | CHAR(32) | 否 | - |
| `expires` | DATETIME(6) | 否 | 过期时间 |
| `scope` | LONGTEXT | 否 | 作用域 |
| `created` | DATETIME(6) | 否 | - |
| `updated` | DATETIME(6) | 否 | - |
| `application_id` | BIGINT | 是 | application 的关联 ID |
| `user_id` | CHAR(32) | 是 | 用户 ID |

**索引：**

- PRIMARY KEY: id
- UNIQUE `jti`: jti
- INDEX `jti`: jti
- INDEX `oauth2_provider_idto_application_id_08c5ff4f_fk_oauth2_pr`: application_id
- INDEX `oauth2_provider_idtoken_user_id_dd512b59_fk_users_user_id`: user_id
- FK `oauth2_provider_idto_application_id_08c5ff4f_fk_oauth2_pr`: application_id → `oauth2_provider_application`.id
- FK `oauth2_provider_idtoken_user_id_dd512b59_fk_users_user_id`: user_id → `users_user`.id

---

### `oauth2_provider_refreshtoken`

**OAuth2 刷新令牌**

| 字段 | 类型 | 可空 | 说明 |
| --- | --- | --- | --- |
| `id` | BIGINT | 否 | 主键，UUID 格式（无连字符，32 位） |
| `token` | VARCHAR(255) | 否 | 令牌 |
| `access_token_id` | BIGINT | 是 | access_token 的关联 ID |
| `application_id` | BIGINT | 否 | application 的关联 ID |
| `user_id` | CHAR(32) | 否 | 用户 ID |
| `created` | DATETIME(6) | 否 | - |
| `updated` | DATETIME(6) | 否 | - |
| `revoked` | DATETIME(6) | 是 | 是否已撤销 |

**索引：**

- PRIMARY KEY: id
- UNIQUE `access_token_id`: access_token_id
- UNIQUE `oauth2_provider_refreshtoken_token_revoked_af8a5134_uniq`: token,revoked
- INDEX `access_token_id`: access_token_id
- INDEX `oauth2_provider_refreshtoken_token_revoked_af8a5134_uniq`: token,revoked
- INDEX `oauth2_provider_refr_application_id_2d1c311b_fk_oauth2_pr`: application_id
- INDEX `oauth2_provider_refreshtoken_user_id_da837fce_fk_users_user_id`: user_id
- FK `oauth2_provider_refr_access_token_id_775e84e8_fk_oauth2_pr`: access_token_id → `oauth2_provider_accesstoken`.id
- FK `oauth2_provider_refr_application_id_2d1c311b_fk_oauth2_pr`: application_id → `oauth2_provider_application`.id
- FK `oauth2_provider_refreshtoken_user_id_da837fce_fk_users_user_id`: user_id → `users_user`.id

---

## 运维作业（Ops）

作业任务、Ad-hoc 命令、Playbook 执行管理

### `ops_adhoc`

**Ad-hoc 命令执行记录**

| 字段 | 类型 | 可空 | 说明 |
| --- | --- | --- | --- |
| `created_by` | VARCHAR(128) | 是 | 创建者用户名 |
| `updated_by` | VARCHAR(128) | 是 | 最后更新者用户名 |
| `date_created` | DATETIME(6) | 是 | Date created |
| `date_updated` | DATETIME(6) | 否 | 更新时间 |
| `id` | CHAR(32) | 否 | Status |
| `name` | VARCHAR(128) | 否 | Name |
| `pattern` | VARCHAR(1024) | 否 | Module |
| `module` | VARCHAR(128) | 否 | Module |
| `args` | VARCHAR(8192) | 否 | Args |
| `comment` | VARCHAR(1024) | 是 | Comment |
| `creator_id` | CHAR(32) | 是 | creator 的关联 ID |
| `scope` | VARCHAR(64) | 否 | Scope |

**索引：**

- PRIMARY KEY: id
- UNIQUE `ops_adhoc_name_creator_id_05bf0c13_uniq`: name,creator_id
- INDEX `ops_adhoc_name_creator_id_05bf0c13_uniq`: name,creator_id
- INDEX `ops_adhoc_creator_id_752f4ac3_fk_users_user_id`: creator_id
- FK `ops_adhoc_creator_id_752f4ac3_fk_users_user_id`: creator_id → `users_user`.id

---

### `ops_celerytask`

**Celery 异步任务记录**

| 字段 | 类型 | 可空 | 说明 |
| --- | --- | --- | --- |
| `id` | CHAR(32) | 否 | Status |
| `name` | VARCHAR(1024) | 否 | Name |
| `date_last_publish` | DATETIME(6) | 是 | Last Publish时间 |

**索引：**

- PRIMARY KEY: id

---

### `ops_celerytaskexecution`

**Celery 任务执行记录**

| 字段 | 类型 | 可空 | 说明 |
| --- | --- | --- | --- |
| `id` | CHAR(32) | 否 | Status |
| `name` | VARCHAR(1024) | 否 | Name |
| `args` | LONGTEXT | 否 | Args |
| `kwargs` | LONGTEXT | 否 | Creator |
| `state` | VARCHAR(16) | 否 | Creator |
| `is_finished` | BOOLEAN | 否 | Creator |
| `date_published` | DATETIME(6) | 否 | Date published |
| `date_start` | DATETIME(6) | 是 | Date start |
| `date_finished` | DATETIME(6) | 是 | Date finished |
| `creator_id` | CHAR(32) | 是 | creator 的关联 ID |

**索引：**

- PRIMARY KEY: id
- INDEX `ops_celerytaskexecution_creator_id_3ea35f11`: creator_id

---

### `ops_historicaljob`

**历史任务记录**

| 字段 | 类型 | 可空 | 说明 |
| --- | --- | --- | --- |
| `created_by` | VARCHAR(128) | 是 | 创建者用户名 |
| `updated_by` | VARCHAR(128) | 是 | 最后更新者用户名 |
| `date_created` | DATETIME(6) | 是 | Date created |
| `date_updated` | DATETIME(6) | 否 | 更新时间 |
| `id` | CHAR(32) | 否 | Status |
| `org_id` | VARCHAR(36) | 否 | 所属组织 ID，用于多租户数据隔离 |
| `is_periodic` | BOOLEAN | 否 | Periodic标记 |
| `interval` | INT | 是 | - |
| `crontab` | VARCHAR(128) | 否 | - |
| `name` | VARCHAR(128) | 是 | Name |
| `instant` | BOOLEAN | 否 | Args |
| `args` | VARCHAR(8192) | 是 | Args |
| `module` | VARCHAR(128) | 是 | Module |
| `chdir` | VARCHAR(1024) | 是 | Run dir |
| `timeout` | INT | 否 | Timeout (Seconds) |
| `type` | VARCHAR(128) | 否 | Variable type |
| `use_parameter_define` | BOOLEAN | 否 | Parameters define |
| `parameters_define` | LONGTEXT | 否 | Parameters define |
| `runas` | VARCHAR(128) | 否 | Run as |
| `runas_policy` | VARCHAR(128) | 否 | Run as policy |
| `comment` | VARCHAR(1024) | 是 | Comment |
| `version` | INT | 否 | 版本号 |
| `history_id` | INT | 否 | history 的关联 ID |
| `history_date` | DATETIME(6) | 否 | - |
| `history_change_reason` | VARCHAR(100) | 是 | - |
| `history_type` | VARCHAR(1) | 否 | - |
| `creator_id` | CHAR(32) | 是 | creator 的关联 ID |
| `history_user_id` | CHAR(32) | 是 | history_user 的关联 ID |
| `playbook_id` | CHAR(32) | 是 | playbook 的关联 ID |
| `periodic_variable` | LONGTEXT | 否 | Periodic variable |
| `start_time` | DATETIME(6) | 是 | - |

**索引：**

- PRIMARY KEY: history_id
- INDEX `ops_historicaljob_id_2bcb4391`: id
- INDEX `ops_historicaljob_org_id_c347a096`: org_id
- INDEX `ops_historicaljob_history_date_1de38f93`: history_date
- INDEX `ops_historicaljob_history_user_id_24f73504_fk_users_user_id`: history_user_id
- INDEX `ops_historicaljob_creator_id_aaf6cde7`: creator_id
- INDEX `ops_historicaljob_playbook_id_2998dc45`: playbook_id
- FK `ops_historicaljob_history_user_id_24f73504_fk_users_user_id`: history_user_id → `users_user`.id

---

### `ops_job`

**作业任务定义**

| 字段 | 类型 | 可空 | 说明 |
| --- | --- | --- | --- |
| `created_by` | VARCHAR(128) | 是 | 创建者用户名 |
| `updated_by` | VARCHAR(128) | 是 | 最后更新者用户名 |
| `date_created` | DATETIME(6) | 是 | Date created |
| `date_updated` | DATETIME(6) | 否 | 更新时间 |
| `id` | CHAR(32) | 否 | Status |
| `org_id` | VARCHAR(36) | 否 | 所属组织 ID，用于多租户数据隔离 |
| `is_periodic` | BOOLEAN | 否 | Periodic标记 |
| `interval` | INT | 是 | - |
| `crontab` | VARCHAR(128) | 否 | - |
| `name` | VARCHAR(128) | 是 | Name |
| `instant` | BOOLEAN | 否 | Args |
| `args` | VARCHAR(8192) | 是 | Args |
| `module` | VARCHAR(128) | 是 | Module |
| `chdir` | VARCHAR(1024) | 是 | Run dir |
| `timeout` | INT | 否 | Timeout (Seconds) |
| `type` | VARCHAR(128) | 否 | Variable type |
| `use_parameter_define` | BOOLEAN | 否 | Parameters define |
| `parameters_define` | LONGTEXT | 否 | Parameters define |
| `runas` | VARCHAR(128) | 否 | Run as |
| `runas_policy` | VARCHAR(128) | 否 | Run as policy |
| `comment` | VARCHAR(1024) | 是 | Comment |
| `version` | INT | 否 | 版本号 |
| `creator_id` | CHAR(32) | 是 | creator 的关联 ID |
| `playbook_id` | CHAR(32) | 是 | playbook 的关联 ID |
| `periodic_variable` | LONGTEXT | 否 | Periodic variable |
| `start_time` | DATETIME(6) | 是 | - |

**索引：**

- PRIMARY KEY: id
- UNIQUE `ops_job_name_org_id_creator_id_type_d236dee6_uniq`: name,org_id,creator_id,type
- INDEX `ops_job_name_org_id_creator_id_type_d236dee6_uniq`: name,org_id,creator_id,type
- INDEX `ops_job_org_id_0e25ddb8`: org_id
- INDEX `ops_job_creator_id_a2f2bc66_fk_users_user_id`: creator_id
- INDEX `ops_job_playbook_id_678fa32d_fk_ops_playbook_id`: playbook_id
- FK `ops_job_creator_id_a2f2bc66_fk_users_user_id`: creator_id → `users_user`.id
- FK `ops_job_playbook_id_678fa32d_fk_ops_playbook_id`: playbook_id → `ops_playbook`.id

---

### `ops_job_assets`

**作业与资产的多对多关联**

| 字段 | 类型 | 可空 | 说明 |
| --- | --- | --- | --- |
| `id` | INT | 否 | Status |
| `job_id` | CHAR(32) | 否 | job 的关联 ID |
| `asset_id` | CHAR(32) | 否 | 关联资产 ID |

**索引：**

- PRIMARY KEY: id
- UNIQUE `ops_job_assets_job_id_asset_id_a12c9edb_uniq`: job_id,asset_id
- INDEX `ops_job_assets_job_id_asset_id_a12c9edb_uniq`: job_id,asset_id
- INDEX `ops_job_assets_asset_id_357d00bf_fk_assets_asset_id`: asset_id
- FK `ops_job_assets_asset_id_357d00bf_fk_assets_asset_id`: asset_id → `assets_asset`.id
- FK `ops_job_assets_job_id_4078e66a_fk_ops_job_id`: job_id → `ops_job`.id

---

### `ops_job_nodes`

**作业与节点的多对多关联**

| 字段 | 类型 | 可空 | 说明 |
| --- | --- | --- | --- |
| `id` | INT | 否 | Status |
| `job_id` | CHAR(32) | 否 | job 的关联 ID |
| `node_id` | CHAR(32) | 否 | node 的关联 ID |

**索引：**

- PRIMARY KEY: id
- UNIQUE `ops_job_nodes_job_id_node_id_e1655349_uniq`: job_id,node_id
- INDEX `ops_job_nodes_job_id_node_id_e1655349_uniq`: job_id,node_id
- INDEX `ops_job_nodes_node_id_1068c496_fk_assets_node_id`: node_id
- FK `ops_job_nodes_job_id_92614179_fk_ops_job_id`: job_id → `ops_job`.id
- FK `ops_job_nodes_node_id_1068c496_fk_assets_node_id`: node_id → `assets_node`.id

---

### `ops_jobexecution`

**作业执行记录**

| 字段 | 类型 | 可空 | 说明 |
| --- | --- | --- | --- |
| `created_by` | VARCHAR(128) | 是 | 创建者用户名 |
| `updated_by` | VARCHAR(128) | 是 | 最后更新者用户名 |
| `date_updated` | DATETIME(6) | 否 | 更新时间 |
| `comment` | LONGTEXT | 否 | Comment |
| `org_id` | VARCHAR(36) | 否 | 所属组织 ID，用于多租户数据隔离 |
| `id` | CHAR(32) | 否 | Status |
| `task_id` | CHAR(32) | 是 | Status |
| `status` | VARCHAR(16) | 否 | Status |
| `job_version` | INT | 否 | Parameters |
| `parameters` | LONGTEXT | 否 | Parameters |
| `result` | LONGTEXT | 是 | Result |
| `summary` | LONGTEXT | 否 | Summary |
| `date_created` | DATETIME(6) | 否 | Date created |
| `date_start` | DATETIME(6) | 是 | Date start |
| `date_finished` | DATETIME(6) | 是 | Date finished |
| `material` | VARCHAR(8192) | 是 | Material |
| `job_type` | VARCHAR(128) | 否 | - |
| `creator_id` | CHAR(32) | 是 | creator 的关联 ID |
| `job_id` | CHAR(32) | 是 | job 的关联 ID |

**索引：**

- PRIMARY KEY: id
- INDEX `ops_jobexecution_org_id_de9582a3`: org_id
- INDEX `ops_jobexecution_date_start_d5a3aa89`: date_start
- INDEX `ops_jobexecution_creator_id_86f1606d_fk_users_user_id`: creator_id
- INDEX `ops_jobexecution_job_id_b7480764_fk_ops_job_id`: job_id
- FK `ops_jobexecution_creator_id_86f1606d_fk_users_user_id`: creator_id → `users_user`.id
- FK `ops_jobexecution_job_id_b7480764_fk_ops_job_id`: job_id → `ops_job`.id

---

### `ops_playbook`

**Ansible Playbook 定义**

| 字段 | 类型 | 可空 | 说明 |
| --- | --- | --- | --- |
| `created_by` | VARCHAR(128) | 是 | 创建者用户名 |
| `updated_by` | VARCHAR(128) | 是 | 最后更新者用户名 |
| `date_created` | DATETIME(6) | 是 | Date created |
| `date_updated` | DATETIME(6) | 否 | 更新时间 |
| `id` | CHAR(32) | 否 | Status |
| `name` | VARCHAR(128) | 是 | Name |
| `path` | VARCHAR(100) | 否 | 路径 |
| `comment` | VARCHAR(1024) | 是 | Comment |
| `create_method` | VARCHAR(128) | 否 | CreateMethod |
| `vcs_url` | VARCHAR(1024) | 是 | VCS URL |
| `creator_id` | CHAR(32) | 是 | creator 的关联 ID |
| `scope` | VARCHAR(64) | 否 | Scope |

**索引：**

- PRIMARY KEY: id
- UNIQUE `ops_playbook_name_creator_id_93345e09_uniq`: name,creator_id
- INDEX `ops_playbook_name_creator_id_93345e09_uniq`: name,creator_id
- INDEX `ops_playbook_creator_id_bc8eec56_fk_users_user_id`: creator_id
- FK `ops_playbook_creator_id_bc8eec56_fk_users_user_id`: creator_id → `users_user`.id

---

### `ops_variable`

**作业变量定义**

| 字段 | 类型 | 可空 | 说明 |
| --- | --- | --- | --- |
| `created_by` | VARCHAR(128) | 是 | 创建者用户名 |
| `updated_by` | VARCHAR(128) | 是 | 最后更新者用户名 |
| `date_created` | DATETIME(6) | 是 | Date created |
| `date_updated` | DATETIME(6) | 否 | 更新时间 |
| `comment` | LONGTEXT | 否 | Comment |
| `id` | CHAR(32) | 否 | Status |
| `name` | VARCHAR(1024) | 是 | Name |
| `var_name` | VARCHAR(1024) | 是 | Variable name |
| `default_value` | VARCHAR(2048) | 是 | Default Value |
| `type` | VARCHAR(64) | 否 | Variable type |
| `tips` | VARCHAR(1024) | 是 | Tips |
| `required` | BOOLEAN | 否 | Required |
| `extra_args` | LONGTEXT | 否 | ExtraVars |
| `adhoc_id` | CHAR(32) | 是 | adhoc 的关联 ID |
| `creator_id` | CHAR(32) | 是 | creator 的关联 ID |
| `job_id` | CHAR(32) | 是 | job 的关联 ID |
| `playbook_id` | CHAR(32) | 是 | playbook 的关联 ID |

**索引：**

- PRIMARY KEY: id
- INDEX `ops_variable_adhoc_id_0ad610ae_fk_ops_adhoc_id`: adhoc_id
- INDEX `ops_variable_creator_id_e5bbf269_fk_users_user_id`: creator_id
- INDEX `ops_variable_job_id_fd9c3a9e_fk_ops_job_id`: job_id
- INDEX `ops_variable_playbook_id_636e4f0d_fk_ops_playbook_id`: playbook_id
- FK `ops_variable_adhoc_id_0ad610ae_fk_ops_adhoc_id`: adhoc_id → `ops_adhoc`.id
- FK `ops_variable_creator_id_e5bbf269_fk_users_user_id`: creator_id → `users_user`.id
- FK `ops_variable_job_id_fd9c3a9e_fk_ops_job_id`: job_id → `ops_job`.id
- FK `ops_variable_playbook_id_636e4f0d_fk_ops_playbook_id`: playbook_id → `ops_playbook`.id

---

## 组织管理（Organizations）

多租户组织隔离

### `orgs_organization`

**组织（多租户隔离单元）**

| 字段 | 类型 | 可空 | 说明 |
| --- | --- | --- | --- |
| `created_by` | VARCHAR(128) | 是 | 创建者用户名 |
| `updated_by` | VARCHAR(128) | 是 | 最后更新者用户名 |
| `date_created` | DATETIME(6) | 是 | 创建时间 |
| `date_updated` | DATETIME(6) | 否 | 更新时间 |
| `comment` | LONGTEXT | 否 | 备注 |
| `id` | CHAR(32) | 否 | 主键，UUID 格式（无连字符，32 位） |
| `name` | VARCHAR(128) | 否 | Builtin |
| `builtin` | BOOLEAN | 否 | Builtin |

**索引：**

- PRIMARY KEY: id
- UNIQUE `name`: name
- INDEX `name`: name

---

## 权限管理（Perms）

资产授权权限管理

### `perms_assetpermission`

**资产授权权限**

| 字段 | 类型 | 可空 | 说明 |
| --- | --- | --- | --- |
| `created_by` | VARCHAR(128) | 是 | 创建者用户名 |
| `updated_by` | VARCHAR(128) | 是 | 最后更新者用户名 |
| `date_created` | DATETIME(6) | 是 | 创建时间 |
| `date_updated` | DATETIME(6) | 否 | 更新时间 |
| `comment` | LONGTEXT | 否 | 备注 |
| `id` | CHAR(32) | 否 | ID |
| `org_id` | VARCHAR(36) | 否 | 所属组织 ID，用于多租户数据隔离 |
| `name` | VARCHAR(128) | 否 | Name |
| `accounts` | LONGTEXT | 否 | Date expired |
| `protocols` | LONGTEXT | 否 | Date expired |
| `actions` | INT | 否 | Date expired |
| `date_start` | DATETIME(6) | 否 | Date expired |
| `date_expired` | DATETIME(6) | 否 | Date expired |
| `is_active` | BOOLEAN | 否 | Active |
| `from_ticket` | BOOLEAN | 否 | From ticket |

**索引：**

- PRIMARY KEY: id
- UNIQUE `perms_assetpermission_org_id_name_b3d2f01b_uniq`: org_id,name
- INDEX `perms_assetpermission_org_id_name_b3d2f01b_uniq`: org_id,name
- INDEX `perms_assetpermission_org_id_9f38f32c`: org_id
- INDEX `perms_assetpermission_date_start_d7ac30e1`: date_start
- INDEX `perms_assetpermission_date_expired_c79fc11f`: date_expired

---

### `perms_assetpermission_assets`

**资产授权与资产的多对多关联**

| 字段 | 类型 | 可空 | 说明 |
| --- | --- | --- | --- |
| `id` | INT | 否 | ID |
| `assetpermission_id` | CHAR(32) | 否 | assetpermission 的关联 ID |
| `asset_id` | CHAR(32) | 否 | 关联资产 ID |

**索引：**

- PRIMARY KEY: id
- UNIQUE `perms_assetpermission_as_assetpermission_id_asset_adf6202c_uniq`: assetpermission_id,asset_id
- INDEX `perms_assetpermission_as_assetpermission_id_asset_adf6202c_uniq`: assetpermission_id,asset_id
- INDEX `perms_assetpermissio_asset_id_d6920078_fk_assets_as`: asset_id
- FK `perms_assetpermissio_asset_id_d6920078_fk_assets_as`: asset_id → `assets_asset`.id
- FK `perms_assetpermissio_assetpermission_id_df023b5e_fk_perms_ass`: assetpermission_id → `perms_assetpermission`.id

---

### `perms_assetpermission_nodes`

**资产授权与节点的多对多关联**

| 字段 | 类型 | 可空 | 说明 |
| --- | --- | --- | --- |
| `id` | INT | 否 | ID |
| `assetpermission_id` | CHAR(32) | 否 | assetpermission 的关联 ID |
| `node_id` | CHAR(32) | 否 | node 的关联 ID |

**索引：**

- PRIMARY KEY: id
- UNIQUE `perms_assetpermission_no_assetpermission_id_node__47f2e539_uniq`: assetpermission_id,node_id
- INDEX `perms_assetpermission_no_assetpermission_id_node__47f2e539_uniq`: assetpermission_id,node_id
- INDEX `perms_assetpermission_nodes_node_id_6b6f1697_fk_assets_node_id`: node_id
- FK `perms_assetpermissio_assetpermission_id_368de545_fk_perms_ass`: assetpermission_id → `perms_assetpermission`.id
- FK `perms_assetpermission_nodes_node_id_6b6f1697_fk_assets_node_id`: node_id → `assets_node`.id

---

### `perms_assetpermission_user_groups`

**资产授权与用户组的多对多关联**

| 字段 | 类型 | 可空 | 说明 |
| --- | --- | --- | --- |
| `id` | INT | 否 | ID |
| `assetpermission_id` | CHAR(32) | 否 | assetpermission 的关联 ID |
| `usergroup_id` | CHAR(32) | 否 | usergroup 的关联 ID |

**索引：**

- PRIMARY KEY: id
- UNIQUE `perms_assetpermission_us_assetpermission_id_userg_e11c51d6_uniq`: assetpermission_id,usergroup_id
- INDEX `perms_assetpermission_us_assetpermission_id_userg_e11c51d6_uniq`: assetpermission_id,usergroup_id
- INDEX `perms_assetpermissio_usergroup_id_42dcdc91_fk_users_use`: usergroup_id
- FK `perms_assetpermissio_assetpermission_id_1fb2ddd3_fk_perms_ass`: assetpermission_id → `perms_assetpermission`.id
- FK `perms_assetpermissio_usergroup_id_42dcdc91_fk_users_use`: usergroup_id → `users_usergroup`.id

---

### `perms_assetpermission_users`

**资产授权与用户的多对多关联**

| 字段 | 类型 | 可空 | 说明 |
| --- | --- | --- | --- |
| `id` | INT | 否 | ID |
| `assetpermission_id` | CHAR(32) | 否 | assetpermission 的关联 ID |
| `user_id` | CHAR(32) | 否 | 用户 ID |

**索引：**

- PRIMARY KEY: id
- UNIQUE `perms_assetpermission_us_assetpermission_id_user__3f3f1eaa_uniq`: assetpermission_id,user_id
- INDEX `perms_assetpermission_us_assetpermission_id_user__3f3f1eaa_uniq`: assetpermission_id,user_id
- INDEX `perms_assetpermission_users_user_id_ba17aecc_fk_users_user_id`: user_id
- FK `perms_assetpermissio_assetpermission_id_1f874915_fk_perms_ass`: assetpermission_id → `perms_assetpermission`.id
- FK `perms_assetpermission_users_user_id_ba17aecc_fk_users_user_id`: user_id → `users_user`.id

---

### `perms_userassetgrantedtreenoderelation`

**用户资产授权树节点关系**

| 字段 | 类型 | 可空 | 说明 |
| --- | --- | --- | --- |
| `id` | INT | 否 | ID |
| `created_by` | VARCHAR(128) | 是 | 创建者用户名 |
| `updated_by` | VARCHAR(128) | 是 | 最后更新者用户名 |
| `date_created` | DATETIME(6) | 是 | 创建时间 |
| `date_updated` | DATETIME(6) | 否 | 更新时间 |
| `org_id` | VARCHAR(36) | 否 | 所属组织 ID，用于多租户数据隔离 |
| `node_key` | VARCHAR(64) | 否 | Parent key |
| `node_parent_key` | VARCHAR(64) | 否 | Parent key |
| `node_from` | VARCHAR(16) | 否 | - |
| `node_assets_amount` | INT | 否 | - |
| `node_id` | CHAR(32) | 否 | node 的关联 ID |
| `user_id` | CHAR(32) | 否 | 用户 ID |

**索引：**

- PRIMARY KEY: id
- INDEX `perms_userassetgrantedtreenoderelation_org_id_b5e76b66`: org_id
- INDEX `perms_userassetgrantedtreenoderelation_node_key_db373db6`: node_key
- INDEX `perms_userassetgrantedtreenoderelation_node_parent_key_3c7651a0`: node_parent_key
- INDEX `perms_userassetgrantedtreenoderelation_node_from_725273e2`: node_from
- INDEX `perms_userassetgrantedtreenoderelation_node_id_75f5af62`: node_id
- INDEX `perms_userassetgrantedtreenoderelation_user_id_fd11b13b`: user_id

---

## RBAC 角色（RBAC）

基于角色的访问控制

### `rbac_menupermission`

**菜单权限定义**

| 字段 | 类型 | 可空 | 说明 |
| --- | --- | --- | --- |
| `id` | CHAR(32) | 否 | Menu permission |

**索引：**

- PRIMARY KEY: id

---

### `rbac_role`

**RBAC 角色定义**

| 字段 | 类型 | 可空 | 说明 |
| --- | --- | --- | --- |
| `created_by` | VARCHAR(128) | 是 | 创建者用户名 |
| `updated_by` | VARCHAR(128) | 是 | 最后更新者用户名 |
| `date_created` | DATETIME(6) | 是 | 创建时间 |
| `date_updated` | DATETIME(6) | 否 | 更新时间 |
| `id` | CHAR(32) | 否 | Menu permission |
| `name` | VARCHAR(128) | 否 | Name |
| `scope` | VARCHAR(128) | 否 | Scope |
| `builtin` | BOOLEAN | 否 | Builtin |
| `comment` | LONGTEXT | 否 | Comment |

**索引：**

- PRIMARY KEY: id
- UNIQUE `rbac_role_name_scope_f7fbc3c9_uniq`: name,scope
- INDEX `rbac_role_name_scope_f7fbc3c9_uniq`: name,scope

---

### `rbac_role_permissions`

**角色与权限的多对多关联**

| 字段 | 类型 | 可空 | 说明 |
| --- | --- | --- | --- |
| `id` | INT | 否 | Menu permission |
| `role_id` | CHAR(32) | 否 | 角色 ID |
| `permission_id` | INT | 否 | permission 的关联 ID |

**索引：**

- PRIMARY KEY: id
- UNIQUE `rbac_role_permissions_role_id_permission_id_d01303da_uniq`: role_id,permission_id
- INDEX `rbac_role_permissions_role_id_permission_id_d01303da_uniq`: role_id,permission_id
- INDEX `rbac_role_permission_permission_id_f5e1e866_fk_auth_perm`: permission_id
- FK `rbac_role_permission_permission_id_f5e1e866_fk_auth_perm`: permission_id → `auth_permission`.id
- FK `rbac_role_permissions_role_id_d10416cb_fk_rbac_role_id`: role_id → `rbac_role`.id

---

### `rbac_rolebinding`

**角色绑定（用户/用户组与角色的关联）**

| 字段 | 类型 | 可空 | 说明 |
| --- | --- | --- | --- |
| `created_by` | VARCHAR(128) | 是 | 创建者用户名 |
| `updated_by` | VARCHAR(128) | 是 | 最后更新者用户名 |
| `date_created` | DATETIME(6) | 是 | 创建时间 |
| `date_updated` | DATETIME(6) | 否 | 更新时间 |
| `comment` | LONGTEXT | 否 | Comment |
| `id` | CHAR(32) | 否 | Menu permission |
| `scope` | VARCHAR(128) | 否 | Scope |
| `org_id` | CHAR(32) | 是 | 所属组织 ID，用于多租户数据隔离 |
| `role_id` | CHAR(32) | 否 | 角色 ID |
| `user_id` | CHAR(32) | 否 | 用户 ID |

**索引：**

- PRIMARY KEY: id
- UNIQUE `rbac_rolebinding_user_id_role_id_org_id_7b7308f9_uniq`: user_id,role_id,org_id
- INDEX `rbac_rolebinding_user_id_role_id_org_id_7b7308f9_uniq`: user_id,role_id,org_id
- INDEX `rbac_rolebinding_org_id_8103bc19_fk_orgs_organization_id`: org_id
- INDEX `rbac_rolebinding_role_id_79cc1751_fk_rbac_role_id`: role_id
- FK `rbac_rolebinding_org_id_8103bc19_fk_orgs_organization_id`: org_id → `orgs_organization`.id
- FK `rbac_rolebinding_role_id_79cc1751_fk_rbac_role_id`: role_id → `rbac_role`.id
- FK `rbac_rolebinding_user_id_d01064f7_fk_users_user_id`: user_id → `users_user`.id

---

## 报表（Reports）

自定义报表

### `reports_report`

**报表定义**

| 字段 | 类型 | 可空 | 说明 |
| --- | --- | --- | --- |
| `created_by` | VARCHAR(128) | 是 | 创建者用户名 |
| `updated_by` | VARCHAR(128) | 是 | 最后更新者用户名 |
| `date_created` | DATETIME(6) | 是 | 创建时间 |
| `date_updated` | DATETIME(6) | 否 | 更新时间 |
| `comment` | LONGTEXT | 否 | 备注 |
| `id` | CHAR(32) | 否 | 主键，UUID 格式（无连字符，32 位） |
| `org_id` | VARCHAR(36) | 否 | 所属组织 ID，用于多租户数据隔离 |
| `name` | VARCHAR(128) | 否 | Name |
| `tp` | VARCHAR(64) | 否 | Type |
| `is_builtin` | BOOLEAN | 否 | Is builtin |
| `is_active` | BOOLEAN | 否 | Is active |
| `days` | INT(10) UNSIGNED | 否 | Range days |
| `filters` | LONGTEXT | 否 | Filters |

**索引：**

- PRIMARY KEY: id
- UNIQUE `reports_report_org_id_name_192c1286_uniq`: org_id,name
- INDEX `reports_report_org_id_name_192c1286_uniq`: org_id,name
- INDEX `reports_report_org_id_3b235c3d`: org_id

---

## 系统设置（Settings）

系统配置项 KV 存储、Chat AI 提示词

### `settings_chatprompt`

**Chat AI 提示词模板**

| 字段 | 类型 | 可空 | 说明 |
| --- | --- | --- | --- |
| `created_by` | VARCHAR(128) | 是 | 创建者用户名 |
| `updated_by` | VARCHAR(128) | 是 | 最后更新者用户名 |
| `date_created` | DATETIME(6) | 是 | 创建时间 |
| `date_updated` | DATETIME(6) | 否 | 更新时间 |
| `comment` | LONGTEXT | 否 | 备注 |
| `id` | CHAR(32) | 否 | 主键，UUID 格式（无连字符，32 位） |
| `name` | VARCHAR(128) | 否 | Name |
| `content` | LONGTEXT | 否 | Content |
| `builtin` | BOOLEAN | 否 | Builtin |

**索引：**

- PRIMARY KEY: id
- UNIQUE `name`: name
- INDEX `name`: name

---

### `settings_setting`

**系统设置（KV 存储）**

| 字段 | 类型 | 可空 | 说明 |
| --- | --- | --- | --- |
| `id` | INT | 否 | 主键，UUID 格式（无连字符，32 位） |
| `name` | VARCHAR(128) | 否 | Name |
| `value` | LONGTEXT | 是 | Category |
| `category` | VARCHAR(128) | 否 | Category |
| `encrypted` | BOOLEAN | 否 | Encrypted |
| `enabled` | BOOLEAN | 否 | 是否启用 |
| `comment` | LONGTEXT | 否 | 备注 |

**索引：**

- PRIMARY KEY: id
- UNIQUE `name`: name
- INDEX `name`: name

---

## 终端会话（Terminal）

会话管理、录像回放、命令记录、应用发布、接入端点等

### `terminal_applet`

**应用（远程应用定义）**

| 字段 | 类型 | 可空 | 说明 |
| --- | --- | --- | --- |
| `created_by` | VARCHAR(128) | 是 | 创建者用户名 |
| `updated_by` | VARCHAR(128) | 是 | 最后更新者用户名 |
| `date_created` | DATETIME(6) | 是 | 创建时间 |
| `date_updated` | DATETIME(6) | 否 | 更新时间 |
| `id` | CHAR(32) | 否 | 主键，UUID 格式（无连字符，32 位） |
| `name` | VARCHAR(128) | 否 | Name |
| `display_name` | VARCHAR(128) | 否 | Display name |
| `version` | VARCHAR(16) | 否 | Version |
| `author` | VARCHAR(128) | 否 | Author |
| `edition` | VARCHAR(128) | 否 | Edition |
| `type` | VARCHAR(16) | 否 | Type |
| `is_active` | BOOLEAN | 否 | Active |
| `builtin` | BOOLEAN | 否 | Builtin |
| `protocols` | LONGTEXT | 否 | Protocol |
| `can_concurrent` | BOOLEAN | 否 | Can concurrent |
| `tags` | LONGTEXT | 否 | Tags |
| `comment` | LONGTEXT | 否 | Comment |

**索引：**

- PRIMARY KEY: id
- UNIQUE `name`: name
- INDEX `name`: name

---

### `terminal_applethost`

**应用发布机（托管远程应用的主机）**

| 字段 | 类型 | 可空 | 说明 |
| --- | --- | --- | --- |
| `host_ptr_id` | CHAR(32) | 否 | host_ptr 的关联 ID |
| `deploy_options` | LONGTEXT | 否 | Deploy options |
| `auto_create_accounts` | BOOLEAN | 否 | Auto create accounts |
| `accounts_create_amount` | INT | 否 | Accounts create amount |
| `inited` | BOOLEAN | 否 | Inited |
| `date_inited` | DATETIME(6) | 是 | Date inited |
| `date_synced` | DATETIME(6) | 是 | Date synced |
| `using_same_account` | BOOLEAN | 否 | Using same account |
| `terminal_id` | CHAR(32) | 是 | terminal 的关联 ID |

**索引：**

- PRIMARY KEY: host_ptr_id
- UNIQUE `terminal_id`: terminal_id
- INDEX `terminal_id`: terminal_id
- FK `terminal_applethost_host_ptr_id_1b2e200b_fk_assets_ho`: host_ptr_id → `assets_host`.asset_ptr_id
- FK `terminal_applethost_terminal_id_0a67b317_fk_terminal_id`: terminal_id → `terminal`.id

---

### `terminal_applethostdeployment`

**应用发布机部署配置**

| 字段 | 类型 | 可空 | 说明 |
| --- | --- | --- | --- |
| `created_by` | VARCHAR(128) | 是 | 创建者用户名 |
| `updated_by` | VARCHAR(128) | 是 | 最后更新者用户名 |
| `date_created` | DATETIME(6) | 是 | 创建时间 |
| `date_updated` | DATETIME(6) | 否 | 更新时间 |
| `id` | CHAR(32) | 否 | 主键，UUID 格式（无连字符，32 位） |
| `initial` | BOOLEAN | 否 | Initial |
| `status` | VARCHAR(16) | 否 | Status |
| `date_start` | DATETIME(6) | 是 | Date start |
| `date_finished` | DATETIME(6) | 是 | Comment |
| `comment` | LONGTEXT | 否 | Comment |
| `task` | CHAR(32) | 是 | Task |
| `host_id` | CHAR(32) | 否 | host 的关联 ID |

**索引：**

- PRIMARY KEY: id
- INDEX `terminal_applethostdeployment_date_start_8f0847d0`: date_start
- INDEX `terminal_applethostd_host_id_a517cbd3_fk_terminal_`: host_id
- FK `terminal_applethostd_host_id_a517cbd3_fk_terminal_`: host_id → `terminal_applethost`.host_ptr_id

---

### `terminal_appletpublication`

**应用发布记录（应用与发布机的关联）**

| 字段 | 类型 | 可空 | 说明 |
| --- | --- | --- | --- |
| `created_by` | VARCHAR(128) | 是 | 创建者用户名 |
| `updated_by` | VARCHAR(128) | 是 | 最后更新者用户名 |
| `date_created` | DATETIME(6) | 是 | 创建时间 |
| `date_updated` | DATETIME(6) | 否 | 更新时间 |
| `id` | CHAR(32) | 否 | 主键，UUID 格式（无连字符，32 位） |
| `status` | VARCHAR(16) | 否 | Status |
| `comment` | LONGTEXT | 否 | Comment |
| `applet_id` | CHAR(32) | 否 | applet 的关联 ID |
| `host_id` | CHAR(32) | 否 | host 的关联 ID |

**索引：**

- PRIMARY KEY: id
- UNIQUE `terminal_appletpublication_applet_id_host_id_96fdf64c_uniq`: applet_id,host_id
- INDEX `terminal_appletpublication_applet_id_host_id_96fdf64c_uniq`: applet_id,host_id
- INDEX `terminal_appletpubli_host_id_3c885a74_fk_terminal_`: host_id
- FK `terminal_appletpubli_applet_id_4d1e569c_fk_terminal_`: applet_id → `terminal_applet`.id
- FK `terminal_appletpubli_host_id_3c885a74_fk_terminal_`: host_id → `terminal_applethost`.host_ptr_id

---

### `terminal_appprovider`

**应用提供商配置**

| 字段 | 类型 | 可空 | 说明 |
| --- | --- | --- | --- |
| `created_by` | VARCHAR(128) | 是 | 创建者用户名 |
| `updated_by` | VARCHAR(128) | 是 | 最后更新者用户名 |
| `date_created` | DATETIME(6) | 是 | 创建时间 |
| `date_updated` | DATETIME(6) | 否 | 更新时间 |
| `comment` | LONGTEXT | 否 | Comment |
| `id` | CHAR(32) | 否 | 主键，UUID 格式（无连字符，32 位） |
| `name` | VARCHAR(128) | 否 | Name |
| `hostname` | VARCHAR(128) | 否 | Hostname |
| `terminal_id` | CHAR(32) | 是 | terminal 的关联 ID |

**索引：**

- PRIMARY KEY: id
- UNIQUE `name`: name
- UNIQUE `terminal_id`: terminal_id
- INDEX `name`: name
- INDEX `terminal_id`: terminal_id
- FK `terminal_appprovider_terminal_id_b1b3b6d2_fk_terminal_id`: terminal_id → `terminal`.id

---

### `terminal_command`

**命令执行记录（审计）**

| 字段 | 类型 | 可空 | 说明 |
| --- | --- | --- | --- |
| `org_id` | VARCHAR(36) | 否 | 所属组织 ID，用于多租户数据隔离 |
| `id` | CHAR(32) | 否 | 主键，UUID 格式（无连字符，32 位） |
| `user` | VARCHAR(64) | 否 | Application User |
| `asset` | VARCHAR(128) | 否 | 资产 |
| `account` | VARCHAR(64) | 否 | 账户 |
| `input` | VARCHAR(128) | 否 | 输入内容 |
| `output` | VARCHAR(1024) | 否 | 命令输出 |
| `session` | VARCHAR(36) | 否 | Session |
| `risk_level` | SMALLINT | 否 | 风险等级 |
| `timestamp` | INT | 否 | - |

**索引：**

- PRIMARY KEY: id
- INDEX `terminal_command_org_id_b29da48e`: org_id
- INDEX `terminal_command_user_62507ff6`: user
- INDEX `terminal_command_asset_a8743384`: asset
- INDEX `terminal_command_account_b319d47e`: account
- INDEX `terminal_command_input_9acfd946`: input
- INDEX `terminal_command_session_62eaa2c3`: session
- INDEX `terminal_command_risk_level_570e11b6`: risk_level
- INDEX `terminal_command_timestamp_85bc8045`: timestamp
- INDEX `idx_timestamp_org`: timestamp,org_id

---

### `terminal_commandstorage`

**命令存储配置**

| 字段 | 类型 | 可空 | 说明 |
| --- | --- | --- | --- |
| `created_by` | VARCHAR(128) | 是 | 创建者用户名 |
| `updated_by` | VARCHAR(128) | 是 | 最后更新者用户名 |
| `date_created` | DATETIME(6) | 是 | 创建时间 |
| `date_updated` | DATETIME(6) | 否 | 更新时间 |
| `comment` | LONGTEXT | 否 | Comment |
| `id` | CHAR(32) | 否 | 主键，UUID 格式（无连字符，32 位） |
| `name` | VARCHAR(128) | 否 | Name |
| `meta` | LONGTEXT | 否 | 元数据 |
| `is_default` | BOOLEAN | 否 | 是否默认值 |
| `type` | VARCHAR(16) | 否 | Type |

**索引：**

- PRIMARY KEY: id
- UNIQUE `name`: name
- INDEX `name`: name

---

### `terminal_endpoint`

**终端接入端点配置**

| 字段 | 类型 | 可空 | 说明 |
| --- | --- | --- | --- |
| `created_by` | VARCHAR(128) | 是 | 创建者用户名 |
| `updated_by` | VARCHAR(128) | 是 | 最后更新者用户名 |
| `date_created` | DATETIME(6) | 是 | 创建时间 |
| `date_updated` | DATETIME(6) | 否 | 更新时间 |
| `id` | CHAR(32) | 否 | 主键，UUID 格式（无连字符，32 位） |
| `name` | VARCHAR(128) | 否 | Name |
| `host` | VARCHAR(256) | 否 | Hosting |
| `https_port` | INT | 否 | - |
| `http_port` | INT | 否 | - |
| `ssh_port` | INT | 否 | - |
| `rdp_port` | INT | 否 | - |
| `mysql_port` | INT | 否 | - |
| `mariadb_port` | INT | 否 | - |
| `postgresql_port` | INT | 否 | - |
| `redis_port` | INT | 否 | - |
| `sqlserver_port` | INT | 否 | - |
| `comment` | LONGTEXT | 否 | Comment |
| `is_active` | BOOLEAN | 否 | Active |
| `vnc_port` | INT | 否 | - |
| `oracle_port` | INT | 否 | - |
| `mongodb_port` | INT | 否 | - |

**索引：**

- PRIMARY KEY: id
- UNIQUE `name`: name
- INDEX `name`: name

---

### `terminal_endpointrule`

**终端接入规则**

| 字段 | 类型 | 可空 | 说明 |
| --- | --- | --- | --- |
| `created_by` | VARCHAR(128) | 是 | 创建者用户名 |
| `updated_by` | VARCHAR(128) | 是 | 最后更新者用户名 |
| `date_created` | DATETIME(6) | 是 | 创建时间 |
| `date_updated` | DATETIME(6) | 否 | 更新时间 |
| `id` | CHAR(32) | 否 | 主键，UUID 格式（无连字符，32 位） |
| `name` | VARCHAR(128) | 否 | Name |
| `ip_group` | LONGTEXT | 否 | IP group |
| `priority` | INT | 否 | Comment |
| `comment` | LONGTEXT | 否 | Comment |
| `is_active` | BOOLEAN | 否 | Active |
| `endpoint_id` | CHAR(32) | 是 | endpoint 的关联 ID |

**索引：**

- PRIMARY KEY: id
- UNIQUE `name`: name
- UNIQUE `priority`: priority
- INDEX `name`: name
- INDEX `priority`: priority
- INDEX `terminal_endpointrul_endpoint_id_69dfcdf2_fk_terminal_`: endpoint_id
- FK `terminal_endpointrul_endpoint_id_69dfcdf2_fk_terminal_`: endpoint_id → `terminal_endpoint`.id

---

### `terminal_replaystorage`

**会话录像存储配置**

| 字段 | 类型 | 可空 | 说明 |
| --- | --- | --- | --- |
| `created_by` | VARCHAR(128) | 是 | 创建者用户名 |
| `updated_by` | VARCHAR(128) | 是 | 最后更新者用户名 |
| `date_created` | DATETIME(6) | 是 | 创建时间 |
| `date_updated` | DATETIME(6) | 否 | 更新时间 |
| `comment` | LONGTEXT | 否 | Comment |
| `id` | CHAR(32) | 否 | 主键，UUID 格式（无连字符，32 位） |
| `name` | VARCHAR(128) | 否 | Name |
| `meta` | LONGTEXT | 否 | 元数据 |
| `is_default` | BOOLEAN | 否 | 是否默认值 |
| `type` | VARCHAR(16) | 否 | Type |

**索引：**

- PRIMARY KEY: id
- UNIQUE `name`: name
- INDEX `name`: name

---

### `terminal_session`

**会话记录（资产连接会话）**

| 字段 | 类型 | 可空 | 说明 |
| --- | --- | --- | --- |
| `org_id` | VARCHAR(36) | 否 | 所属组织 ID，用于多租户数据隔离 |
| `id` | CHAR(32) | 否 | 主键，UUID 格式（无连字符，32 位） |
| `user` | VARCHAR(128) | 否 | Application User |
| `user_id` | VARCHAR(36) | 否 | 用户 ID |
| `asset` | VARCHAR(128) | 否 | 资产 |
| `asset_id` | VARCHAR(36) | 否 | 关联资产 ID |
| `account` | VARCHAR(128) | 否 | 账户 |
| `account_id` | VARCHAR(128) | 否 | account 的关联 ID |
| `protocol` | VARCHAR(16) | 否 | 协议（ssh/rdp/vnc/telnet） |
| `login_from` | VARCHAR(2) | 否 | Success |
| `type` | VARCHAR(16) | 否 | Type |
| `remote_addr` | VARCHAR(128) | 是 | Success |
| `is_success` | BOOLEAN | 否 | Success |
| `is_finished` | BOOLEAN | 否 | Finished |
| `has_replay` | BOOLEAN | 否 | 是否有录像 |
| `has_command` | BOOLEAN | 否 | 是否有命令记录 |
| `date_start` | DATETIME(6) | 否 | Date start |
| `date_end` | DATETIME(6) | 是 | 结束时间 |
| `comment` | LONGTEXT | 是 | Comment |
| `cmd_amount` | INT | 否 | - |
| `error_reason` | VARCHAR(128) | 否 | - |
| `terminal_id` | CHAR(32) | 是 | terminal 的关联 ID |
| `replay_size` | BIGINT | 否 | - |

**索引：**

- PRIMARY KEY: id
- INDEX `terminal_session_org_id_9e113282`: org_id
- INDEX `terminal_session_user_6910eb8f`: user
- INDEX `terminal_session_user_id_a0fe42e0`: user_id
- INDEX `terminal_session_asset_fe247cfd`: asset
- INDEX `terminal_session_asset_id_f655dd49`: asset_id
- INDEX `terminal_session_account_3e975ce8`: account
- INDEX `terminal_session_account_id_b72ef6f8`: account_id
- INDEX `terminal_session_protocol_3181452c`: protocol
- INDEX `terminal_session_type_d749168b`: type
- INDEX `terminal_session_is_success_13e3ce88`: is_success
- INDEX `terminal_session_is_finished_a89c8792`: is_finished
- INDEX `terminal_session_date_start_5c59d95b`: date_start
- INDEX `terminal_session_terminal_id_5278f31c`: terminal_id

---

### `terminal_sessionjoinrecord`

**会话加入记录（会话共享）**

| 字段 | 类型 | 可空 | 说明 |
| --- | --- | --- | --- |
| `created_by` | VARCHAR(128) | 是 | 创建者用户名 |
| `updated_by` | VARCHAR(128) | 是 | 最后更新者用户名 |
| `date_created` | DATETIME(6) | 是 | 创建时间 |
| `date_updated` | DATETIME(6) | 否 | 更新时间 |
| `comment` | LONGTEXT | 否 | Comment |
| `id` | CHAR(32) | 否 | 主键，UUID 格式（无连字符，32 位） |
| `org_id` | VARCHAR(36) | 否 | 所属组织 ID，用于多租户数据隔离 |
| `verify_code` | VARCHAR(16) | 否 | Verify code |
| `date_joined` | DATETIME(6) | 否 | 加入时间 |
| `date_left` | DATETIME(6) | 是 | Success |
| `remote_addr` | VARCHAR(128) | 是 | Success |
| `login_from` | VARCHAR(2) | 否 | Success |
| `is_success` | BOOLEAN | 否 | Success |
| `reason` | VARCHAR(1024) | 是 | Reason |
| `is_finished` | BOOLEAN | 否 | Finished |
| `joiner_id` | CHAR(32) | 是 | joiner 的关联 ID |
| `session_id` | CHAR(32) | 否 | session 的关联 ID |
| `sharing_id` | CHAR(32) | 否 | sharing 的关联 ID |

**索引：**

- PRIMARY KEY: id
- INDEX `terminal_sessionjoinrecord_org_id_053ec401`: org_id
- INDEX `terminal_sessionjoinrecord_date_joined_1b50df56`: date_joined
- INDEX `terminal_sessionjoinrecord_date_left_c71ae289`: date_left
- INDEX `terminal_sessionjoinrecord_remote_addr_e975ba2a`: remote_addr
- INDEX `terminal_sessionjoinrecord_is_success_7c817cde`: is_success
- INDEX `terminal_sessionjoinrecord_is_finished_d4adf288`: is_finished
- INDEX `terminal_sessionjoinrecord_joiner_id_72515369_fk_users_user_id`: joiner_id
- INDEX `terminal_sessionjoin_session_id_52f46320_fk_terminal_`: session_id
- INDEX `terminal_sessionjoin_sharing_id_32e6c9f5_fk_terminal_`: sharing_id
- FK `terminal_sessionjoin_session_id_52f46320_fk_terminal_`: session_id → `terminal_session`.id
- FK `terminal_sessionjoin_sharing_id_32e6c9f5_fk_terminal_`: sharing_id → `terminal_sessionsharing`.id
- FK `terminal_sessionjoinrecord_joiner_id_72515369_fk_users_user_id`: joiner_id → `users_user`.id

---

### `terminal_sessionreplay`

**会话录像（回放文件）**

| 字段 | 类型 | 可空 | 说明 |
| --- | --- | --- | --- |
| `created_by` | VARCHAR(128) | 是 | 创建者用户名 |
| `updated_by` | VARCHAR(128) | 是 | 最后更新者用户名 |
| `date_created` | DATETIME(6) | 是 | 创建时间 |
| `date_updated` | DATETIME(6) | 否 | 更新时间 |
| `comment` | LONGTEXT | 否 | Comment |
| `id` | CHAR(32) | 否 | 主键，UUID 格式（无连字符，32 位） |
| `session_id` | CHAR(32) | 否 | session 的关联 ID |

**索引：**

- PRIMARY KEY: id
- INDEX `terminal_sessionrepl_session_id_228568d3_fk_terminal_`: session_id
- FK `terminal_sessionrepl_session_id_228568d3_fk_terminal_`: session_id → `terminal_session`.id

---

### `terminal_sessionsharing`

**会话共享配置**

| 字段 | 类型 | 可空 | 说明 |
| --- | --- | --- | --- |
| `created_by` | VARCHAR(128) | 是 | 创建者用户名 |
| `updated_by` | VARCHAR(128) | 是 | 最后更新者用户名 |
| `date_created` | DATETIME(6) | 是 | 创建时间 |
| `date_updated` | DATETIME(6) | 否 | 更新时间 |
| `comment` | LONGTEXT | 否 | Comment |
| `id` | CHAR(32) | 否 | 主键，UUID 格式（无连字符，32 位） |
| `org_id` | VARCHAR(36) | 否 | 所属组织 ID，用于多租户数据隔离 |
| `verify_code` | VARCHAR(16) | 否 | Verify code |
| `is_active` | BOOLEAN | 否 | Active |
| `expired_time` | INT | 否 | Expired time (min) |
| `users` | LONGTEXT | 否 | Action permission |
| `action_permission` | VARCHAR(16) | 否 | Action permission |
| `origin` | VARCHAR(200) | 是 | Origin |
| `creator_id` | CHAR(32) | 是 | creator 的关联 ID |
| `session_id` | CHAR(32) | 否 | session 的关联 ID |

**索引：**

- PRIMARY KEY: id
- INDEX `terminal_sessionsharing_org_id_0b959af3`: org_id
- INDEX `terminal_sessionsharing_is_active_c604d0ce`: is_active
- INDEX `terminal_sessionsharing_expired_time_26d5cf9b`: expired_time
- INDEX `terminal_sessionsharing_creator_id_bb273804_fk_users_user_id`: creator_id
- INDEX `terminal_sessionshar_session_id_f302e994_fk_terminal_`: session_id
- FK `terminal_sessionshar_session_id_f302e994_fk_terminal_`: session_id → `terminal_session`.id
- FK `terminal_sessionsharing_creator_id_bb273804_fk_users_user_id`: creator_id → `users_user`.id

---

### `terminal_status`

**终端状态信息**

| 字段 | 类型 | 可空 | 说明 |
| --- | --- | --- | --- |
| `id` | CHAR(32) | 否 | 主键，UUID 格式（无连字符，32 位） |
| `session_online` | INT | 否 | - |
| `cpu_load` | DOUBLE | 否 | - |
| `memory_used` | DOUBLE | 否 | - |
| `disk_used` | DOUBLE | 否 | - |
| `connections` | INT | 否 | - |
| `threads` | INT | 否 | - |
| `boot_time` | DOUBLE | 否 | - |
| `date_created` | DATETIME(6) | 否 | 创建时间 |
| `terminal_id` | CHAR(32) | 是 | terminal 的关联 ID |

**索引：**

- PRIMARY KEY: id
- INDEX `terminal_status_terminal_id_b57e6176_fk_terminal_id`: terminal_id
- FK `terminal_status_terminal_id_b57e6176_fk_terminal_id`: terminal_id → `terminal`.id

---

### `terminal_task`

**终端任务记录**

| 字段 | 类型 | 可空 | 说明 |
| --- | --- | --- | --- |
| `created_by` | VARCHAR(128) | 是 | 创建者用户名 |
| `updated_by` | VARCHAR(128) | 是 | 最后更新者用户名 |
| `date_created` | DATETIME(6) | 是 | 创建时间 |
| `date_updated` | DATETIME(6) | 否 | 更新时间 |
| `comment` | LONGTEXT | 否 | Comment |
| `id` | CHAR(32) | 否 | 主键，UUID 格式（无连字符，32 位） |
| `name` | VARCHAR(128) | 否 | Name |
| `args` | VARCHAR(1024) | 否 | 参数 |
| `kwargs` | LONGTEXT | 否 | 关键字参数 |
| `is_finished` | BOOLEAN | 否 | Finished |
| `date_finished` | DATETIME(6) | 是 | Comment |
| `terminal_id` | CHAR(32) | 是 | terminal 的关联 ID |

**索引：**

- PRIMARY KEY: id
- INDEX `terminal_task_terminal_id_55577303_fk_terminal_id`: terminal_id
- FK `terminal_task_terminal_id_55577303_fk_terminal_id`: terminal_id → `terminal`.id

---

### `terminal_virtualapp`

**虚拟应用定义**

| 字段 | 类型 | 可空 | 说明 |
| --- | --- | --- | --- |
| `created_by` | VARCHAR(128) | 是 | 创建者用户名 |
| `updated_by` | VARCHAR(128) | 是 | 最后更新者用户名 |
| `date_created` | DATETIME(6) | 是 | 创建时间 |
| `date_updated` | DATETIME(6) | 否 | 更新时间 |
| `id` | CHAR(32) | 否 | 主键，UUID 格式（无连字符，32 位） |
| `name` | VARCHAR(128) | 否 | Name |
| `display_name` | VARCHAR(128) | 否 | Display name |
| `version` | VARCHAR(16) | 否 | Version |
| `author` | VARCHAR(128) | 否 | Author |
| `is_active` | BOOLEAN | 否 | Active |
| `protocols` | LONGTEXT | 否 | Protocol |
| `image_name` | VARCHAR(128) | 否 | Image name |
| `image_protocol` | VARCHAR(16) | 否 | Image protocol |
| `image_port` | INT | 否 | Image port |
| `comment` | LONGTEXT | 否 | Comment |
| `tags` | LONGTEXT | 否 | Tags |

**索引：**

- PRIMARY KEY: id
- UNIQUE `name`: name
- INDEX `name`: name

---

### `terminal_virtualapppublication`

**虚拟应用发布记录**

| 字段 | 类型 | 可空 | 说明 |
| --- | --- | --- | --- |
| `created_by` | VARCHAR(128) | 是 | 创建者用户名 |
| `updated_by` | VARCHAR(128) | 是 | 最后更新者用户名 |
| `date_created` | DATETIME(6) | 是 | 创建时间 |
| `date_updated` | DATETIME(6) | 否 | 更新时间 |
| `comment` | LONGTEXT | 否 | Comment |
| `id` | CHAR(32) | 否 | 主键，UUID 格式（无连字符，32 位） |
| `status` | VARCHAR(16) | 否 | Status |
| `app_id` | CHAR(32) | 否 | app 的关联 ID |
| `provider_id` | CHAR(32) | 否 | provider 的关联 ID |

**索引：**

- PRIMARY KEY: id
- UNIQUE `terminal_virtualapppublication_provider_id_app_id_1a3b5a47_uniq`: provider_id,app_id
- INDEX `terminal_virtualapppublication_provider_id_app_id_1a3b5a47_uniq`: provider_id,app_id
- INDEX `terminal_virtualappp_app_id_4def1236_fk_terminal_`: app_id
- FK `terminal_virtualappp_app_id_4def1236_fk_terminal_`: app_id → `terminal_virtualapp`.id
- FK `terminal_virtualappp_provider_id_5b65af1b_fk_terminal_`: provider_id → `terminal_appprovider`.id

---

## 工单系统（Tickets）

审批工单、申请工单、工单流程管理

### `tickets_applyassetticket`

**申请资产工单**

| 字段 | 类型 | 可空 | 说明 |
| --- | --- | --- | --- |
| `ticket_ptr_id` | CHAR(32) | 否 | ticket_ptr 的关联 ID |
| `apply_permission_name` | VARCHAR(128) | 否 | Permission name |
| `apply_accounts` | LONGTEXT | 否 | Apply accounts |
| `apply_actions` | INT | 否 | Actions |
| `apply_date_start` | DATETIME(6) | 是 | Date start |
| `apply_date_expired` | DATETIME(6) | 是 | Date expired |

**索引：**

- PRIMARY KEY: ticket_ptr_id
- FK `tickets_applyassetti_ticket_ptr_id_1bb5e258_fk_tickets_t`: ticket_ptr_id → `tickets_ticket`.id

---

### `tickets_applyassetticket_apply_assets`

**申请资产工单与资产的关联**

| 字段 | 类型 | 可空 | 说明 |
| --- | --- | --- | --- |
| `id` | INT | 否 | 主键，UUID 格式（无连字符，32 位） |
| `applyassetticket_id` | CHAR(32) | 否 | applyassetticket 的关联 ID |
| `asset_id` | CHAR(32) | 否 | 关联资产 ID |

**索引：**

- PRIMARY KEY: id
- UNIQUE `tickets_applyassetticket_applyassetticket_id_asse_9657d165_uniq`: applyassetticket_id,asset_id
- INDEX `tickets_applyassetticket_applyassetticket_id_asse_9657d165_uniq`: applyassetticket_id,asset_id
- INDEX `tickets_applyassetti_asset_id_9721556c_fk_assets_as`: asset_id
- FK `tickets_applyassetti_applyassetticket_id_1eb1c040_fk_tickets_a`: applyassetticket_id → `tickets_applyassetticket`.ticket_ptr_id
- FK `tickets_applyassetti_asset_id_9721556c_fk_assets_as`: asset_id → `assets_asset`.id

---

### `tickets_applyassetticket_apply_nodes`

**申请资产工单与节点的关联**

| 字段 | 类型 | 可空 | 说明 |
| --- | --- | --- | --- |
| `id` | INT | 否 | 主键，UUID 格式（无连字符，32 位） |
| `applyassetticket_id` | CHAR(32) | 否 | applyassetticket 的关联 ID |
| `node_id` | CHAR(32) | 否 | node 的关联 ID |

**索引：**

- PRIMARY KEY: id
- UNIQUE `tickets_applyassetticket_applyassetticket_id_node_eb3632f6_uniq`: applyassetticket_id,node_id
- INDEX `tickets_applyassetticket_applyassetticket_id_node_eb3632f6_uniq`: applyassetticket_id,node_id
- INDEX `tickets_applyassetti_node_id_c90be137_fk_assets_no`: node_id
- FK `tickets_applyassetti_applyassetticket_id_a1ae4866_fk_tickets_a`: applyassetticket_id → `tickets_applyassetticket`.ticket_ptr_id
- FK `tickets_applyassetti_node_id_c90be137_fk_assets_no`: node_id → `assets_node`.id

---

### `tickets_applycommandticket`

**申请执行命令工单**

| 字段 | 类型 | 可空 | 说明 |
| --- | --- | --- | --- |
| `ticket_ptr_id` | CHAR(32) | 否 | ticket_ptr 的关联 ID |
| `apply_run_asset` | VARCHAR(128) | 否 | Run asset |
| `apply_run_command` | VARCHAR(4096) | 否 | Run command |
| `apply_run_account` | VARCHAR(128) | 否 | Account |
| `apply_from_cmd_filter_acl_id` | CHAR(32) | 是 | apply_from_cmd_filter_acl 的关联 ID |
| `apply_from_session_id` | CHAR(32) | 是 | apply_from_session 的关联 ID |
| `apply_run_user_id` | CHAR(32) | 是 | apply_run_user 的关联 ID |

**索引：**

- PRIMARY KEY: ticket_ptr_id
- INDEX `tickets_applycommand_apply_from_cmd_filte_a18c8e6c_fk_acls_comm`: apply_from_cmd_filter_acl_id
- INDEX `tickets_applycommand_apply_from_session_i_79d4ee87_fk_terminal_`: apply_from_session_id
- INDEX `tickets_applycommand_apply_run_user_id_767a3591_fk_users_use`: apply_run_user_id
- FK `tickets_applycommand_apply_from_cmd_filte_a18c8e6c_fk_acls_comm`: apply_from_cmd_filter_acl_id → `acls_commandfilteracl`.id
- FK `tickets_applycommand_apply_from_session_i_79d4ee87_fk_terminal_`: apply_from_session_id → `terminal_session`.id
- FK `tickets_applycommand_apply_run_user_id_767a3591_fk_users_use`: apply_run_user_id → `users_user`.id
- FK `tickets_applycommand_ticket_ptr_id_b0348a17_fk_tickets_t`: ticket_ptr_id → `tickets_ticket`.id

---

### `tickets_applyloginassetticket`

**申请登录资产工单**

| 字段 | 类型 | 可空 | 说明 |
| --- | --- | --- | --- |
| `ticket_ptr_id` | CHAR(32) | 否 | ticket_ptr 的关联 ID |
| `apply_login_account` | VARCHAR(128) | 否 | Login account |
| `apply_login_asset_id` | CHAR(32) | 是 | apply_login_asset 的关联 ID |
| `apply_login_user_id` | CHAR(32) | 是 | apply_login_user 的关联 ID |

**索引：**

- PRIMARY KEY: ticket_ptr_id
- INDEX `tickets_applyloginas_apply_login_asset_id_10c5f8ac_fk_assets_as`: apply_login_asset_id
- INDEX `tickets_applyloginas_apply_login_user_id_b8667ad6_fk_users_use`: apply_login_user_id
- FK `tickets_applyloginas_apply_login_asset_id_10c5f8ac_fk_assets_as`: apply_login_asset_id → `assets_asset`.id
- FK `tickets_applyloginas_apply_login_user_id_b8667ad6_fk_users_use`: apply_login_user_id → `users_user`.id
- FK `tickets_applyloginas_ticket_ptr_id_e0e739b9_fk_tickets_t`: ticket_ptr_id → `tickets_ticket`.id

---

### `tickets_applyloginticket`

**申请登录工单**

| 字段 | 类型 | 可空 | 说明 |
| --- | --- | --- | --- |
| `ticket_ptr_id` | CHAR(32) | 否 | ticket_ptr 的关联 ID |
| `apply_login_ip` | CHAR(39) | 是 | Login IP |
| `apply_login_city` | VARCHAR(64) | 是 | Login city |
| `apply_login_datetime` | DATETIME(6) | 是 | Login Date |

**索引：**

- PRIMARY KEY: ticket_ptr_id
- FK `tickets_applyloginti_ticket_ptr_id_e012c346_fk_tickets_t`: ticket_ptr_id → `tickets_ticket`.id

---

### `tickets_approvalrule`

**审批规则定义**

| 字段 | 类型 | 可空 | 说明 |
| --- | --- | --- | --- |
| `created_by` | VARCHAR(128) | 是 | 创建者用户名 |
| `updated_by` | VARCHAR(128) | 是 | 最后更新者用户名 |
| `date_created` | DATETIME(6) | 是 | 创建时间 |
| `date_updated` | DATETIME(6) | 否 | 更新时间 |
| `comment` | LONGTEXT | 否 | Comment |
| `id` | CHAR(32) | 否 | 主键，UUID 格式（无连字符，32 位） |
| `level` | SMALLINT | 否 | Approve level |
| `users` | LONGTEXT | 否 | 授权用户 |

**索引：**

- PRIMARY KEY: id

---

### `tickets_comment`

**工单评论**

| 字段 | 类型 | 可空 | 说明 |
| --- | --- | --- | --- |
| `created_by` | VARCHAR(128) | 是 | 创建者用户名 |
| `updated_by` | VARCHAR(128) | 是 | 最后更新者用户名 |
| `date_created` | DATETIME(6) | 是 | 创建时间 |
| `date_updated` | DATETIME(6) | 否 | 更新时间 |
| `comment` | LONGTEXT | 否 | Comment |
| `id` | CHAR(32) | 否 | 主键，UUID 格式（无连字符，32 位） |
| `user_display` | VARCHAR(256) | 否 | 用户显示 |
| `body` | LONGTEXT | 否 | 请求体 |
| `type` | VARCHAR(16) | 否 | Type |
| `state` | VARCHAR(16) | 是 | State |
| `ticket_id` | CHAR(32) | 否 | ticket 的关联 ID |
| `user_id` | CHAR(32) | 是 | 用户 ID |

**索引：**

- PRIMARY KEY: id
- INDEX `tickets_comment_ticket_id_36a9497d_fk_tickets_ticket_id`: ticket_id
- INDEX `tickets_comment_user_id_9bf2a162_fk_users_user_id`: user_id
- FK `tickets_comment_ticket_id_36a9497d_fk_tickets_ticket_id`: ticket_id → `tickets_ticket`.id
- FK `tickets_comment_user_id_9bf2a162_fk_users_user_id`: user_id → `users_user`.id

---

### `tickets_ticket`

**工单主表**

| 字段 | 类型 | 可空 | 说明 |
| --- | --- | --- | --- |
| `created_by` | VARCHAR(128) | 是 | 创建者用户名 |
| `updated_by` | VARCHAR(128) | 是 | 最后更新者用户名 |
| `date_created` | DATETIME(6) | 是 | 创建时间 |
| `date_updated` | DATETIME(6) | 否 | 更新时间 |
| `id` | CHAR(32) | 否 | 主键，UUID 格式（无连字符，32 位） |
| `title` | VARCHAR(256) | 否 | Title |
| `type` | VARCHAR(64) | 否 | Type |
| `state` | VARCHAR(16) | 否 | State |
| `status` | VARCHAR(16) | 否 | Status |
| `approval_step` | SMALLINT | 否 | Approval step |
| `comment` | LONGTEXT | 否 | Comment |
| `rel_snapshot` | LONGTEXT | 否 | Relation snapshot |
| `serial_num` | VARCHAR(128) | 是 | Organization |
| `meta` | LONGTEXT | 否 | Organization |
| `org_id` | VARCHAR(36) | 否 | Organization |
| `applicant_id` | CHAR(32) | 是 | applicant 的关联 ID |
| `flow_id` | CHAR(32) | 是 | flow 的关联 ID |

**索引：**

- PRIMARY KEY: id
- UNIQUE `tickets_ticket_serial_num_7efc1f36_uniq`: serial_num
- INDEX `tickets_ticket_serial_num_7efc1f36_uniq`: serial_num
- INDEX `tickets_ticket_org_id_56b25ecf`: org_id
- INDEX `tickets_ticket_applicant_id_65687995_fk_users_user_id`: applicant_id
- INDEX `tickets_ticket_flow_id_da99d17e_fk_tickets_ticketflow_id`: flow_id
- FK `tickets_ticket_applicant_id_65687995_fk_users_user_id`: applicant_id → `users_user`.id
- FK `tickets_ticket_flow_id_da99d17e_fk_tickets_ticketflow_id`: flow_id → `tickets_ticketflow`.id

---

### `tickets_ticketassignee`

**工单审批人**

| 字段 | 类型 | 可空 | 说明 |
| --- | --- | --- | --- |
| `created_by` | VARCHAR(128) | 是 | 创建者用户名 |
| `updated_by` | VARCHAR(128) | 是 | 最后更新者用户名 |
| `date_created` | DATETIME(6) | 是 | 创建时间 |
| `date_updated` | DATETIME(6) | 否 | 更新时间 |
| `comment` | LONGTEXT | 否 | Comment |
| `id` | CHAR(32) | 否 | 主键，UUID 格式（无连字符，32 位） |
| `state` | VARCHAR(64) | 否 | State |
| `assignee_id` | CHAR(32) | 否 | assignee 的关联 ID |
| `step_id` | CHAR(32) | 否 | step 的关联 ID |

**索引：**

- PRIMARY KEY: id
- INDEX `tickets_ticketassignee_assignee_id_101526d4_fk_users_user_id`: assignee_id
- INDEX `tickets_ticketassignee_step_id_3c8450ea_fk_tickets_ticketstep_id`: step_id
- FK `tickets_ticketassignee_assignee_id_101526d4_fk_users_user_id`: assignee_id → `users_user`.id
- FK `tickets_ticketassignee_step_id_3c8450ea_fk_tickets_ticketstep_id`: step_id → `tickets_ticketstep`.id

---

### `tickets_ticketflow`

**工单流程定义**

| 字段 | 类型 | 可空 | 说明 |
| --- | --- | --- | --- |
| `created_by` | VARCHAR(128) | 是 | 创建者用户名 |
| `updated_by` | VARCHAR(128) | 是 | 最后更新者用户名 |
| `date_created` | DATETIME(6) | 是 | 创建时间 |
| `date_updated` | DATETIME(6) | 否 | 更新时间 |
| `comment` | LONGTEXT | 否 | Comment |
| `id` | CHAR(32) | 否 | 主键，UUID 格式（无连字符，32 位） |
| `org_id` | VARCHAR(36) | 否 | Organization |
| `type` | VARCHAR(64) | 否 | Type |
| `approval_level` | SMALLINT | 否 | Approve level |

**索引：**

- PRIMARY KEY: id
- INDEX `tickets_ticketflow_org_id_b1721dd8`: org_id

---

### `tickets_ticketflow_rules`

**工单流程与规则的关联**

| 字段 | 类型 | 可空 | 说明 |
| --- | --- | --- | --- |
| `id` | INT | 否 | 主键，UUID 格式（无连字符，32 位） |
| `ticketflow_id` | CHAR(32) | 否 | ticketflow 的关联 ID |
| `approvalrule_id` | CHAR(32) | 否 | approvalrule 的关联 ID |

**索引：**

- PRIMARY KEY: id
- UNIQUE `tickets_ticketflow_rules_ticketflow_id_approvalru_5b79ffa9_uniq`: ticketflow_id,approvalrule_id
- INDEX `tickets_ticketflow_rules_ticketflow_id_approvalru_5b79ffa9_uniq`: ticketflow_id,approvalrule_id
- INDEX `tickets_ticketflow_r_approvalrule_id_933c985d_fk_tickets_a`: approvalrule_id
- FK `tickets_ticketflow_r_approvalrule_id_933c985d_fk_tickets_a`: approvalrule_id → `tickets_approvalrule`.id
- FK `tickets_ticketflow_r_ticketflow_id_7b158e76_fk_tickets_t`: ticketflow_id → `tickets_ticketflow`.id

---

### `tickets_ticketsession`

**工单会话**

| 字段 | 类型 | 可空 | 说明 |
| --- | --- | --- | --- |
| `id` | INT | 否 | 主键，UUID 格式（无连字符，32 位） |
| `session_id` | CHAR(32) | 否 | session 的关联 ID |
| `ticket_id` | CHAR(32) | 否 | ticket 的关联 ID |

**索引：**

- PRIMARY KEY: id
- INDEX `tickets_ticketsession_session_id_3a6350fd`: session_id
- INDEX `tickets_ticketsession_ticket_id_f0e2ab03`: ticket_id

---

### `tickets_ticketstep`

**工单步骤**

| 字段 | 类型 | 可空 | 说明 |
| --- | --- | --- | --- |
| `created_by` | VARCHAR(128) | 是 | 创建者用户名 |
| `updated_by` | VARCHAR(128) | 是 | 最后更新者用户名 |
| `date_created` | DATETIME(6) | 是 | 创建时间 |
| `date_updated` | DATETIME(6) | 否 | 更新时间 |
| `comment` | LONGTEXT | 否 | Comment |
| `id` | CHAR(32) | 否 | 主键，UUID 格式（无连字符，32 位） |
| `level` | SMALLINT | 否 | Approve level |
| `state` | VARCHAR(64) | 否 | State |
| `status` | VARCHAR(16) | 否 | Status |
| `ticket_id` | CHAR(32) | 否 | ticket 的关联 ID |

**索引：**

- PRIMARY KEY: id
- INDEX `tickets_ticketstep_ticket_id_860309c6_fk_tickets_ticket_id`: ticket_id
- FK `tickets_ticketstep_ticket_id_860309c6_fk_tickets_ticket_id`: ticket_id → `tickets_ticket`.id

---

## 用户管理（Users）

用户账户、用户组、密码历史、偏好设置

### `users_preference`

**用户偏好设置**

| 字段 | 类型 | 可空 | 说明 |
| --- | --- | --- | --- |
| `id` | INT | 否 | 主键，UUID 格式（无连字符，32 位） |
| `name` | VARCHAR(128) | 否 | Name |
| `category` | VARCHAR(128) | 否 | Category |
| `value` | LONGTEXT | 否 | Encrypted |
| `encrypted` | BOOLEAN | 否 | Encrypted |
| `user_id` | CHAR(32) | 否 | 用户 ID |

**索引：**

- PRIMARY KEY: id
- UNIQUE `users_preference_name_user_id_ff36dae0_uniq`: name,user_id
- INDEX `users_preference_name_user_id_ff36dae0_uniq`: name,user_id
- INDEX `users_preference_user_id_309a5b5a_fk_users_user_id`: user_id
- FK `users_preference_user_id_309a5b5a_fk_users_user_id`: user_id → `users_user`.id

---

### `users_user`

**用户主表**

| 字段 | 类型 | 可空 | 说明 |
| --- | --- | --- | --- |
| `password` | VARCHAR(128) | 否 | 密码 |
| `last_login` | DATETIME(6) | 是 | 最后登录 |
| `first_name` | VARCHAR(150) | 否 | 名 |
| `last_name` | VARCHAR(150) | 否 | 姓 |
| `is_active` | BOOLEAN | 否 | 是否启用 |
| `date_joined` | DATETIME(6) | 否 | 加入时间 |
| `id` | CHAR(32) | 否 | 主键，UUID 格式（无连字符，32 位） |
| `username` | VARCHAR(128) | 否 | 用户名 |
| `name` | VARCHAR(128) | 否 | Name |
| `email` | VARCHAR(256) | 否 | 邮箱地址 |
| `role` | VARCHAR(10) | 否 | 角色 |
| `is_service_account` | BOOLEAN | 否 | 是否为服务账号 |
| `avatar` | VARCHAR(100) | 是 | 用户头像 URL |
| `wechat` | VARCHAR(256) | 否 | - |
| `phone` | VARCHAR(256) | 是 | 手机号码 |
| `mfa_level` | SMALLINT | 否 | 多因素认证等级（0=无/1=全部/2=TOTP） |
| `otp_secret_key` | VARCHAR(256) | 是 | OTP 密钥（用于 TOTP 二次认证） |
| `private_key` | LONGTEXT | 是 | 私钥 |
| `public_key` | LONGTEXT | 是 | 公钥 |
| `comment` | LONGTEXT | 是 | 备注 |
| `is_first_login` | BOOLEAN | 否 | 是否首次登录 |
| `date_expired` | DATETIME(6) | 是 | 过期时间 |
| `created_by` | VARCHAR(30) | 否 | 创建者用户名 |
| `updated_by` | VARCHAR(30) | 否 | 最后更新者用户名 |
| `date_password_last_updated` | DATETIME(6) | 是 | Password Last Updated时间 |
| `need_update_password` | BOOLEAN | 否 | - |
| `source` | VARCHAR(30) | 否 | 来源（local/ldap/oidc 等） |
| `wecom_id` | VARCHAR(128) | 是 | wecom 的关联 ID |
| `dingtalk_id` | VARCHAR(128) | 是 | dingtalk 的关联 ID |
| `feishu_id` | VARCHAR(128) | 是 | feishu 的关联 ID |
| `lark_id` | VARCHAR(128) | 是 | lark 的关联 ID |
| `slack_id` | VARCHAR(128) | 是 | slack 的关联 ID |
| `date_api_key_last_used` | DATETIME(6) | 是 | Api Key Last Used时间 |
| `date_updated` | DATETIME(6) | 否 | 更新时间 |
| `face_vector` | LONGTEXT | 是 | - |
| `email_lookup` | VARCHAR(128) | 是 | - |
| `ukey_sn` | VARCHAR(128) | 是 | - |

**索引：**

- PRIMARY KEY: id
- UNIQUE `username`: username
- UNIQUE `email`: email
- UNIQUE `users_user_lark_id_34fa8617_uniq`: lark_id
- UNIQUE `users_user_slack_id_867c518f_uniq`: slack_id
- UNIQUE `users_user_dingtalk_id_a7f722c4_uniq`: dingtalk_id
- UNIQUE `users_user_wecom_id_cd44382f_uniq`: wecom_id
- UNIQUE `users_user_feishu_id_cc1e204a_uniq`: feishu_id
- UNIQUE `ukey_sn`: ukey_sn
- INDEX `username`: username
- INDEX `email`: email
- INDEX `users_user_lark_id_34fa8617_uniq`: lark_id
- INDEX `users_user_slack_id_867c518f_uniq`: slack_id
- INDEX `users_user_dingtalk_id_a7f722c4_uniq`: dingtalk_id
- INDEX `users_user_wecom_id_cd44382f_uniq`: wecom_id
- INDEX `users_user_feishu_id_cc1e204a_uniq`: feishu_id
- INDEX `ukey_sn`: ukey_sn
- INDEX `users_user_date_expired_2e2eb0b3`: date_expired

---

### `users_user_groups`

**用户与用户组的多对多关联**

| 字段 | 类型 | 可空 | 说明 |
| --- | --- | --- | --- |
| `id` | INT | 否 | 主键，UUID 格式（无连字符，32 位） |
| `user_id` | CHAR(32) | 否 | 用户 ID |
| `usergroup_id` | CHAR(32) | 否 | usergroup 的关联 ID |

**索引：**

- PRIMARY KEY: id
- UNIQUE `users_user_groups_user_id_usergroup_id_ac1e3824_uniq`: user_id,usergroup_id
- INDEX `users_user_groups_user_id_usergroup_id_ac1e3824_uniq`: user_id,usergroup_id
- INDEX `users_user_groups_usergroup_id_90818973_fk_users_usergroup_id`: usergroup_id
- FK `users_user_groups_user_id_5f6f5a90_fk_users_user_id`: user_id → `users_user`.id
- FK `users_user_groups_usergroup_id_90818973_fk_users_usergroup_id`: usergroup_id → `users_usergroup`.id

---

### `users_user_user_permissions`

**用户与权限的多对多关联**

| 字段 | 类型 | 可空 | 说明 |
| --- | --- | --- | --- |
| `id` | INT | 否 | 主键，UUID 格式（无连字符，32 位） |
| `user_id` | CHAR(32) | 否 | 用户 ID |
| `permission_id` | INT | 否 | permission 的关联 ID |

**索引：**

- PRIMARY KEY: id
- UNIQUE `users_user_user_permissions_user_id_permission_id_43338c45_uniq`: user_id,permission_id
- INDEX `users_user_user_permissions_user_id_permission_id_43338c45_uniq`: user_id,permission_id
- INDEX `users_user_user_perm_permission_id_0b93982e_fk_auth_perm`: permission_id
- FK `users_user_user_perm_permission_id_0b93982e_fk_auth_perm`: permission_id → `auth_permission`.id
- FK `users_user_user_permissions_user_id_20aca447_fk_users_user_id`: user_id → `users_user`.id

---

### `users_usergroup`

**用户组定义**

| 字段 | 类型 | 可空 | 说明 |
| --- | --- | --- | --- |
| `created_by` | VARCHAR(128) | 是 | 创建者用户名 |
| `updated_by` | VARCHAR(128) | 是 | 最后更新者用户名 |
| `date_created` | DATETIME(6) | 是 | 创建时间 |
| `date_updated` | DATETIME(6) | 否 | 更新时间 |
| `comment` | LONGTEXT | 否 | 备注 |
| `id` | CHAR(32) | 否 | 主键，UUID 格式（无连字符，32 位） |
| `org_id` | VARCHAR(36) | 否 | 所属组织 ID，用于多租户数据隔离 |
| `name` | VARCHAR(128) | 否 | Name |

**索引：**

- PRIMARY KEY: id
- UNIQUE `users_usergroup_org_id_name_e3d49d01_uniq`: org_id,name
- INDEX `users_usergroup_org_id_name_e3d49d01_uniq`: org_id,name
- INDEX `users_usergroup_org_id_995a56e5`: org_id

---

### `users_userpasswordhistory`

**用户密码历史记录**

| 字段 | 类型 | 可空 | 说明 |
| --- | --- | --- | --- |
| `id` | CHAR(32) | 否 | 主键，UUID 格式（无连字符，32 位） |
| `password` | VARCHAR(128) | 否 | 密码 |
| `date_created` | DATETIME(6) | 否 | 创建时间 |
| `user_id` | CHAR(32) | 否 | 用户 ID |

**索引：**

- PRIMARY KEY: id
- INDEX `users_userpasswordhistory_user_id_d2c011ae_fk_users_user_id`: user_id
- FK `users_userpasswordhistory_user_id_d2c011ae_fk_users_user_id`: user_id → `users_user`.id

---

## 企业版功能（X-Pack）

企业版特有的同步、策略、许可证等功能

### `xpack_account`

**X-Pack 账户（企业版功能）**

| 字段 | 类型 | 可空 | 说明 |
| --- | --- | --- | --- |
| `created_by` | VARCHAR(128) | 是 | 创建者用户名 |
| `updated_by` | VARCHAR(128) | 是 | 最后更新者用户名 |
| `date_created` | DATETIME(6) | 是 | 创建时间 |
| `date_updated` | DATETIME(6) | 否 | 更新时间 |
| `id` | CHAR(32) | 否 | 主键，UUID 格式（无连字符，32 位） |
| `org_id` | VARCHAR(36) | 否 | 所属组织 ID，用于多租户数据隔离 |
| `name` | VARCHAR(128) | 否 | 名称 |
| `provider` | VARCHAR(128) | 否 | - |
| `attrs` | LONGTEXT | 否 | - |
| `validity` | BOOLEAN | 否 | - |
| `comment` | LONGTEXT | 否 | 备注 |
| `category` | VARCHAR(32) | 否 | - |

**索引：**

- PRIMARY KEY: id
- UNIQUE `xpack_account_org_id_name_c920d8ec_uniq`: org_id,name
- INDEX `xpack_account_org_id_name_c920d8ec_uniq`: org_id,name
- INDEX `xpack_account_org_id_a2d9d72a`: org_id

---

### `xpack_interface`

**X-Pack 界面配置**

| 字段 | 类型 | 可空 | 说明 |
| --- | --- | --- | --- |
| `id` | CHAR(32) | 否 | 主键，UUID 格式（无连字符，32 位） |
| `login_title` | VARCHAR(1024) | 是 | - |
| `login_image` | VARCHAR(128) | 是 | - |
| `favicon` | VARCHAR(128) | 是 | - |
| `logo_index` | VARCHAR(128) | 是 | - |
| `logo_logout` | VARCHAR(128) | 是 | - |
| `theme` | VARCHAR(16) | 否 | - |
| `footer_content` | LONGTEXT | 否 | - |
| `ext` | LONGTEXT | 否 | - |

**索引：**

- PRIMARY KEY: id

---

### `xpack_license`

**X-Pack 许可证**

| 字段 | 类型 | 可空 | 说明 |
| --- | --- | --- | --- |
| `id` | CHAR(32) | 否 | 主键，UUID 格式（无连字符，32 位） |
| `content` | LONGTEXT | 否 | 通知内容 |

**索引：**

- PRIMARY KEY: id

---

### `xpack_strategy`

**X-Pack 策略定义**

| 字段 | 类型 | 可空 | 说明 |
| --- | --- | --- | --- |
| `created_by` | VARCHAR(128) | 是 | 创建者用户名 |
| `updated_by` | VARCHAR(128) | 是 | 最后更新者用户名 |
| `date_created` | DATETIME(6) | 是 | 创建时间 |
| `date_updated` | DATETIME(6) | 否 | 更新时间 |
| `comment` | LONGTEXT | 否 | 备注 |
| `org_id` | VARCHAR(36) | 否 | 所属组织 ID，用于多租户数据隔离 |
| `id` | CHAR(32) | 否 | 主键，UUID 格式（无连字符，32 位） |
| `name` | VARCHAR(128) | 否 | 名称 |
| `rule_relation` | VARCHAR(64) | 否 | - |
| `priority` | INT | 否 | 优先级 |
| `category` | VARCHAR(32) | 否 | - |

**索引：**

- PRIMARY KEY: id
- UNIQUE `xpack_strategy_org_id_name_3bd11150_uniq`: org_id,name
- INDEX `xpack_strategy_org_id_name_3bd11150_uniq`: org_id,name
- INDEX `xpack_strategy_org_id_2739a03d`: org_id

---

### `xpack_strategyaction`

**X-Pack 策略动作**

| 字段 | 类型 | 可空 | 说明 |
| --- | --- | --- | --- |
| `org_id` | VARCHAR(36) | 否 | 所属组织 ID，用于多租户数据隔离 |
| `id` | CHAR(32) | 否 | 主键，UUID 格式（无连字符，32 位） |
| `attr` | VARCHAR(64) | 否 | - |
| `value` | LONGTEXT | 否 | 值 |
| `strategy_id` | CHAR(32) | 是 | 策略 ID |

**索引：**

- PRIMARY KEY: id
- INDEX `xpack_strategyaction_strategy_id_102c9c2e_fk_xpack_strategy_id`: strategy_id
- INDEX `xpack_strategyaction_org_id_980c9f52`: org_id
- FK `xpack_strategyaction_strategy_id_102c9c2e_fk_xpack_strategy_id`: strategy_id → `xpack_strategy`.id

---

### `xpack_strategyrule`

**X-Pack 策略规则**

| 字段 | 类型 | 可空 | 说明 |
| --- | --- | --- | --- |
| `org_id` | VARCHAR(36) | 否 | 所属组织 ID，用于多租户数据隔离 |
| `id` | CHAR(32) | 否 | 主键，UUID 格式（无连字符，32 位） |
| `attr` | VARCHAR(64) | 否 | - |
| `match` | VARCHAR(16) | 否 | - |
| `value` | VARCHAR(256) | 否 | 值 |
| `strategy_id` | CHAR(32) | 是 | 策略 ID |

**索引：**

- PRIMARY KEY: id
- INDEX `xpack_strategyrule_strategy_id_bd925013_fk_xpack_strategy_id`: strategy_id
- INDEX `xpack_strategyrule_org_id_13850bdd`: org_id
- FK `xpack_strategyrule_strategy_id_bd925013_fk_xpack_strategy_id`: strategy_id → `xpack_strategy`.id

---

### `xpack_syncinstancedetail`

**X-Pack 同步实例详情**

| 字段 | 类型 | 可空 | 说明 |
| --- | --- | --- | --- |
| `org_id` | VARCHAR(36) | 否 | 所属组织 ID，用于多租户数据隔离 |
| `id` | CHAR(32) | 否 | 主键，UUID 格式（无连字符，32 位） |
| `instance_id` | VARCHAR(128) | 否 | instance 的关联 ID |
| `region` | VARCHAR(128) | 否 | - |
| `status` | SMALLINT | 否 | 状态 |
| `date_sync` | DATETIME(6) | 是 | Sync时间 |
| `asset_id` | CHAR(32) | 是 | 关联资产 ID |
| `execution_id` | CHAR(32) | 否 | 执行记录 ID |
| `task_id` | CHAR(32) | 否 | Celery 任务 ID |

**索引：**

- PRIMARY KEY: id
- INDEX `xpack_syncinstancede_execution_id_cf4433e5_fk_xpack_syn`: execution_id
- INDEX `xpack_syncinstancede_task_id_8b171c79_fk_xpack_syn`: task_id
- INDEX `xpack_syncinstancedetail_org_id_75fdc0b2`: org_id
- INDEX `xpack_syncinstancedetail_asset_id_37fb290b_fk_assets_asset_id`: asset_id
- FK `xpack_syncinstancede_execution_id_cf4433e5_fk_xpack_syn`: execution_id → `xpack_syncinstancetaskexecution`.id
- FK `xpack_syncinstancede_task_id_8b171c79_fk_xpack_syn`: task_id → `xpack_syncinstancetask`.id
- FK `xpack_syncinstancedetail_asset_id_37fb290b_fk_assets_asset_id`: asset_id → `assets_asset`.id

---

### `xpack_syncinstancetask`

**X-Pack 同步实例任务**

| 字段 | 类型 | 可空 | 说明 |
| --- | --- | --- | --- |
| `created_by` | VARCHAR(128) | 是 | 创建者用户名 |
| `updated_by` | VARCHAR(128) | 是 | 最后更新者用户名 |
| `date_created` | DATETIME(6) | 是 | 创建时间 |
| `date_updated` | DATETIME(6) | 否 | 更新时间 |
| `id` | CHAR(32) | 否 | 主键，UUID 格式（无连字符，32 位） |
| `org_id` | VARCHAR(36) | 否 | 所属组织 ID，用于多租户数据隔离 |
| `name` | VARCHAR(128) | 否 | 名称 |
| `is_periodic` | BOOLEAN | 否 | Periodic标记 |
| `interval` | INT | 是 | - |
| `crontab` | VARCHAR(128) | 否 | - |
| `regions` | LONGTEXT | 否 | - |
| `hostname_strategy` | VARCHAR(128) | 否 | - |
| `ip_network_segment_group` | LONGTEXT | 否 | - |
| `sync_ip_type` | INT | 否 | - |
| `is_always_update` | BOOLEAN | 否 | Always Update标记 |
| `fully_synchronous` | BOOLEAN | 否 | - |
| `release_assets` | BOOLEAN | 否 | - |
| `comment` | LONGTEXT | 否 | 备注 |
| `date_last_sync` | DATETIME(6) | 是 | 最后同步时间 |
| `account_id` | CHAR(32) | 是 | account 的关联 ID |
| `start_time` | DATETIME(6) | 是 | - |
| `date_last_run` | DATETIME(6) | 是 | Last Run时间 |

**索引：**

- PRIMARY KEY: id
- UNIQUE `xpack_syncinstancetask_org_id_name_5ee59749_uniq`: org_id,name
- INDEX `xpack_syncinstancetask_org_id_name_5ee59749_uniq`: org_id,name
- INDEX `xpack_syncinstancetask_account_id_2bc27ea7_fk_xpack_account_id`: account_id
- INDEX `xpack_syncinstancetask_org_id_1c2e996c`: org_id
- FK `xpack_syncinstancetask_account_id_2bc27ea7_fk_xpack_account_id`: account_id → `xpack_account`.id

---

### `xpack_syncinstancetask_strategy`

**X-Pack 同步任务与策略的关联**

| 字段 | 类型 | 可空 | 说明 |
| --- | --- | --- | --- |
| `id` | INT | 否 | 主键，UUID 格式（无连字符，32 位） |
| `syncinstancetask_id` | CHAR(32) | 否 | syncinstancetask 的关联 ID |
| `strategy_id` | CHAR(32) | 否 | 策略 ID |

**索引：**

- PRIMARY KEY: id
- UNIQUE `xpack_syncinstancetask_s_syncinstancetask_id_stra_a2909cfc_uniq`: syncinstancetask_id,strategy_id
- INDEX `xpack_syncinstancetask_s_syncinstancetask_id_stra_a2909cfc_uniq`: syncinstancetask_id,strategy_id
- INDEX `xpack_syncinstanceta_strategy_id_fa01faae_fk_xpack_str`: strategy_id
- FK `xpack_syncinstanceta_strategy_id_fa01faae_fk_xpack_str`: strategy_id → `xpack_strategy`.id
- FK `xpack_syncinstanceta_syncinstancetask_id_ddc1442c_fk_xpack_syn`: syncinstancetask_id → `xpack_syncinstancetask`.id

---

### `xpack_syncinstancetaskexecution`

**X-Pack 同步任务执行记录**

| 字段 | 类型 | 可空 | 说明 |
| --- | --- | --- | --- |
| `org_id` | VARCHAR(36) | 否 | 所属组织 ID，用于多租户数据隔离 |
| `id` | CHAR(32) | 否 | 主键，UUID 格式（无连字符，32 位） |
| `result` | LONGTEXT | 否 | 结果 |
| `status` | SMALLINT | 否 | 状态 |
| `reason` | VARCHAR(128) | 否 | - |
| `date_sync` | DATETIME(6) | 是 | Sync时间 |
| `snapshot` | LONGTEXT | 是 | - |
| `task_id` | CHAR(32) | 否 | Celery 任务 ID |
| `trigger` | VARCHAR(128) | 否 | - |

**索引：**

- PRIMARY KEY: id
- INDEX `xpack_syncinstanceta_task_id_18733bee_fk_xpack_syn`: task_id
- INDEX `xpack_syncinstancetaskexecution_org_id_2a83697b`: org_id
- FK `xpack_syncinstanceta_task_id_18733bee_fk_xpack_syn`: task_id → `xpack_syncinstancetask`.id

---
