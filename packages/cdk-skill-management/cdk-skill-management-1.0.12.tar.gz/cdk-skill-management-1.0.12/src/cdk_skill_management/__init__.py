'''
# cdk-skill-management

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Build status](https://img.shields.io/github/actions/workflow/status/t0bst4r/cdk-skill-management/release.yml?logo=github)](https://github.com/t0bst4r/cdk-skill-management)

[![Github version](https://img.shields.io/github/v/release/t0bst4r/cdk-skill-management?logo=github)](https://github.com/t0bst4r/cdk-skill-management)
[![npm](https://img.shields.io/npm/v/cdk-skill-management?logo=npm)](https://www.npmjs.com/package/cdk-skill-management)
[![PyPI version](https://img.shields.io/pypi/v/cdk-skill-management?logo=pypi)](https://pypi.org/project/cdk-skill-management/)

> Since I am only working with Node.js and TypeScript, the Python package is currently not tested / used.
> Therefore I am looking for someone to use and test it to provide feedback, if the library is actually working and if there are best practices to apply (e.g. namings, module name, etc.).

Your library for creating and managing Alexa Skills via CloudFormation using AWS CDK.

## Table of Contents

* [Installation](#installation)
* [Usage](#usage)
* [Contributing](#contributing)
* [License](#license)

## Installation

### Node.js / TypeScript

To install the Node.js version of this library, use npm or yarn:

```bash
npm install cdk-skill-management
# or
yarn add cdk-skill-management
```

### Python

To install the Python version of this library, use pip:

```bash
pip install cdk-skill-management
```

## Usage

To use this library in your AWS CDK project, import and instantiate the classes you need.

### Regional restrictions

Skills can be deployed in every AWS regions, but Lambda Endpoints are restricted to

* North America: `arn:aws:lambda:us-east-1:<aws_account_id>:function:<lambda_name>`
* Europe, India: `arn:aws:lambda:eu-west-1:<aws_account_id>:function:<lambda_name>`
* Far East: `arn:aws:lambda:location<aws_account_id>:function:<lambda_name>`

### CDK deployment order

* You can use `skillPackage.overrides` to patch your lambda function ARN into your skill package.
* Make sure to call `addDependency` on your skill instance.

### Skill Permissions

In order for Alexa to call the skill endpoint - i.e. the Lambda function - a resource based permission must be added to allow the Alexa Service Principal to call the function.
However, this would cause any Alexa Skill to be able to call the endpoint. Therefore, the skill-id should be added as a condition to the permission.

However, when deploying the skill, Alexa immediately checks if the skill endpoint is allowed to be accessed. At this point, we do not have a skill id to add to the resource based permission.

Therefore, this library includes a construct `SkillEndpointPermission`, which first creates a resource based permission that allows Alexa to call `invokeFunction` in general.

After the creation of the Skill, the Skill Id can be injected into the Permission. To do this, simply call the `configureSkillId` method on the `SkillEndpointPermission`.

### Example

Here's an example including the `skillPackage.overrides` and `SkillEndpointPermission`.

```python
import * as cdk from 'aws-cdk-lib';
import * as lambda from 'aws-cdk-lib/aws-lambda';
import * as s3Assets from 'aws-cdk-lib/aws-s3-assets';
import * as secretsmanager from 'aws-cdk-lib/aws-secretsmanager';
import * as ssm from 'aws-cdk-lib/aws-ssm';
import {Construct} from 'constructs';

import * as skill from 'cdk-skill-management';

export class MyStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props: cdk.StackProps = {}) {
    super(scope, id, props);

    const vendorParameter = ssm.StringParameter
      .fromStringParameterName(this, 'VendorIdParameter', 'my-skill-vendor-id');
    const skillCredentials = secretsmanager
      .Secret.fromSecretNameV2(this, 'SkillCredentials', 'my-skill-authentication');
    const asset = new s3Assets.Asset(this, 'SkillPackageAsset', {path: './path/to/my/skill-package'});

    const myFunction = new lambda.Function(this, 'MyEndpointFunction', {...});
    const endpointPermission = new skill.SkillEndpointPermission(this, 'EndpointPermission', {
      handler: myFunction,
      skillType: skill.SkillType.SMART_HOME,
    });

    const mySkill = new skill.Skill(this, 'Skill', {
      skillType: skill.SkillType.SMART_HOME,
      skillStage: 'development',
      vendorId: vendorParameter.stringValue,
      authenticationConfiguration: {
        clientId: skillCredentials.secretValueFromJson('clientId').unsafeUnwrap(),
        clientSecret: skillCredentials.secretValueFromJson('clientSecret').unsafeUnwrap(),
        refreshToken: skillCredentials.secretValueFromJson('refreshToken').unsafeUnwrap(),
      },
      skillPackage: {
        asset,
        overrides: {
          manifest: {
            apis: {
              smartHome: {
                endpoint: {
                  uri: myFunction.functionArn
                }
              }
            }
          }
        }
      },
    });
    mySkill.addDependency(myFunction);
    mySkill.addDependency(endpointPermission);

    endpointPermission.configureSkillId(this, 'EndpointPermissionSkill', mySkill);
  }
}
```

## Contributing

We welcome contributions from the community. To contribute, please follow our [contribution guidelines](CONTRIBUTE.md).

## License

This library is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
'''
import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from typeguard import check_type

from ._jsii import *

import aws_cdk as _aws_cdk_ceddda9d
import aws_cdk.alexa_ask as _aws_cdk_alexa_ask_ceddda9d
import aws_cdk.aws_lambda as _aws_cdk_aws_lambda_ceddda9d
import aws_cdk.aws_s3_assets as _aws_cdk_aws_s3_assets_ceddda9d
import aws_cdk.aws_secretsmanager as _aws_cdk_aws_secretsmanager_ceddda9d
import aws_cdk.aws_ssm as _aws_cdk_aws_ssm_ceddda9d
import constructs as _constructs_77d1e7e8


@jsii.data_type(
    jsii_type="cdk-skill-management.AccountLinkingPlatformAuthorizationUrl",
    jsii_struct_bases=[],
    name_mapping={
        "platform_authorization_url": "platformAuthorizationUrl",
        "platform_type": "platformType",
    },
)
class AccountLinkingPlatformAuthorizationUrl:
    def __init__(
        self,
        *,
        platform_authorization_url: builtins.str,
        platform_type: builtins.str,
    ) -> None:
        '''Represents a platform-specific authorization URL for account linking.

        :param platform_authorization_url: The platform-specific authorization URL.
        :param platform_type: The platform type.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f884dc6d966eaaf535502a58835af4763a09088c8d530d6338e96ed080db5ff)
            check_type(argname="argument platform_authorization_url", value=platform_authorization_url, expected_type=type_hints["platform_authorization_url"])
            check_type(argname="argument platform_type", value=platform_type, expected_type=type_hints["platform_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "platform_authorization_url": platform_authorization_url,
            "platform_type": platform_type,
        }

    @builtins.property
    def platform_authorization_url(self) -> builtins.str:
        '''The platform-specific authorization URL.'''
        result = self._values.get("platform_authorization_url")
        assert result is not None, "Required property 'platform_authorization_url' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def platform_type(self) -> builtins.str:
        '''The platform type.'''
        result = self._values.get("platform_type")
        assert result is not None, "Required property 'platform_type' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AccountLinkingPlatformAuthorizationUrl(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-skill-management.AccountLinkingRequest",
    jsii_struct_bases=[],
    name_mapping={
        "access_token_scheme": "accessTokenScheme",
        "access_token_url": "accessTokenUrl",
        "authentication_flow_type": "authenticationFlowType",
        "authorization_url": "authorizationUrl",
        "authorization_urls_by_platform": "authorizationUrlsByPlatform",
        "client_id": "clientId",
        "client_secret": "clientSecret",
        "default_token_expiration_in_seconds": "defaultTokenExpirationInSeconds",
        "domains": "domains",
        "reciprocal_access_token_url": "reciprocalAccessTokenUrl",
        "redirect_url": "redirectUrl",
        "scopes": "scopes",
        "skip_on_enablement": "skipOnEnablement",
        "voice_forward_account_linking": "voiceForwardAccountLinking",
    },
)
class AccountLinkingRequest:
    def __init__(
        self,
        *,
        access_token_scheme: typing.Optional[builtins.str] = None,
        access_token_url: typing.Optional[builtins.str] = None,
        authentication_flow_type: typing.Optional[builtins.str] = None,
        authorization_url: typing.Optional[builtins.str] = None,
        authorization_urls_by_platform: typing.Optional[typing.Sequence[typing.Union[AccountLinkingPlatformAuthorizationUrl, typing.Dict[builtins.str, typing.Any]]]] = None,
        client_id: typing.Optional[builtins.str] = None,
        client_secret: typing.Optional[builtins.str] = None,
        default_token_expiration_in_seconds: typing.Optional[jsii.Number] = None,
        domains: typing.Optional[typing.Sequence[builtins.str]] = None,
        reciprocal_access_token_url: typing.Optional[builtins.str] = None,
        redirect_url: typing.Optional[typing.Sequence[builtins.str]] = None,
        scopes: typing.Optional[typing.Sequence[builtins.str]] = None,
        skip_on_enablement: typing.Optional[builtins.bool] = None,
        voice_forward_account_linking: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Represents the request parameters for account linking.

        :param access_token_scheme: The access token scheme.
        :param access_token_url: The access token URL for account linking.
        :param authentication_flow_type: The type of account linking.
        :param authorization_url: The authorization URL for account linking.
        :param authorization_urls_by_platform: An array of platform-specific authorization URLs for account linking.
        :param client_id: The client ID for account linking. -
        :param client_secret: The client secret for account linking.
        :param default_token_expiration_in_seconds: The default token expiration in seconds for account linking.
        :param domains: An array of domains for account linking.
        :param reciprocal_access_token_url: The reciprocal access token URL for account linking.
        :param redirect_url: An array of redirect URLs for account linking.
        :param scopes: An array of scopes for account linking.
        :param skip_on_enablement: Indicates whether to skip account linking on enablement.
        :param voice_forward_account_linking: Voice-forward account linking setting, either 'ENABLED' or 'DISABLED'.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c6ec99be4a6947103f12e33db65670189692f73c3aa14e510a48a2e4d30598d9)
            check_type(argname="argument access_token_scheme", value=access_token_scheme, expected_type=type_hints["access_token_scheme"])
            check_type(argname="argument access_token_url", value=access_token_url, expected_type=type_hints["access_token_url"])
            check_type(argname="argument authentication_flow_type", value=authentication_flow_type, expected_type=type_hints["authentication_flow_type"])
            check_type(argname="argument authorization_url", value=authorization_url, expected_type=type_hints["authorization_url"])
            check_type(argname="argument authorization_urls_by_platform", value=authorization_urls_by_platform, expected_type=type_hints["authorization_urls_by_platform"])
            check_type(argname="argument client_id", value=client_id, expected_type=type_hints["client_id"])
            check_type(argname="argument client_secret", value=client_secret, expected_type=type_hints["client_secret"])
            check_type(argname="argument default_token_expiration_in_seconds", value=default_token_expiration_in_seconds, expected_type=type_hints["default_token_expiration_in_seconds"])
            check_type(argname="argument domains", value=domains, expected_type=type_hints["domains"])
            check_type(argname="argument reciprocal_access_token_url", value=reciprocal_access_token_url, expected_type=type_hints["reciprocal_access_token_url"])
            check_type(argname="argument redirect_url", value=redirect_url, expected_type=type_hints["redirect_url"])
            check_type(argname="argument scopes", value=scopes, expected_type=type_hints["scopes"])
            check_type(argname="argument skip_on_enablement", value=skip_on_enablement, expected_type=type_hints["skip_on_enablement"])
            check_type(argname="argument voice_forward_account_linking", value=voice_forward_account_linking, expected_type=type_hints["voice_forward_account_linking"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if access_token_scheme is not None:
            self._values["access_token_scheme"] = access_token_scheme
        if access_token_url is not None:
            self._values["access_token_url"] = access_token_url
        if authentication_flow_type is not None:
            self._values["authentication_flow_type"] = authentication_flow_type
        if authorization_url is not None:
            self._values["authorization_url"] = authorization_url
        if authorization_urls_by_platform is not None:
            self._values["authorization_urls_by_platform"] = authorization_urls_by_platform
        if client_id is not None:
            self._values["client_id"] = client_id
        if client_secret is not None:
            self._values["client_secret"] = client_secret
        if default_token_expiration_in_seconds is not None:
            self._values["default_token_expiration_in_seconds"] = default_token_expiration_in_seconds
        if domains is not None:
            self._values["domains"] = domains
        if reciprocal_access_token_url is not None:
            self._values["reciprocal_access_token_url"] = reciprocal_access_token_url
        if redirect_url is not None:
            self._values["redirect_url"] = redirect_url
        if scopes is not None:
            self._values["scopes"] = scopes
        if skip_on_enablement is not None:
            self._values["skip_on_enablement"] = skip_on_enablement
        if voice_forward_account_linking is not None:
            self._values["voice_forward_account_linking"] = voice_forward_account_linking

    @builtins.property
    def access_token_scheme(self) -> typing.Optional[builtins.str]:
        '''The access token scheme.'''
        result = self._values.get("access_token_scheme")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def access_token_url(self) -> typing.Optional[builtins.str]:
        '''The access token URL for account linking.'''
        result = self._values.get("access_token_url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def authentication_flow_type(self) -> typing.Optional[builtins.str]:
        '''The type of account linking.'''
        result = self._values.get("authentication_flow_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def authorization_url(self) -> typing.Optional[builtins.str]:
        '''The authorization URL for account linking.'''
        result = self._values.get("authorization_url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def authorization_urls_by_platform(
        self,
    ) -> typing.Optional[typing.List[AccountLinkingPlatformAuthorizationUrl]]:
        '''An array of platform-specific authorization URLs for account linking.'''
        result = self._values.get("authorization_urls_by_platform")
        return typing.cast(typing.Optional[typing.List[AccountLinkingPlatformAuthorizationUrl]], result)

    @builtins.property
    def client_id(self) -> typing.Optional[builtins.str]:
        '''The client ID for account linking.

        -
        '''
        result = self._values.get("client_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def client_secret(self) -> typing.Optional[builtins.str]:
        '''The client secret for account linking.'''
        result = self._values.get("client_secret")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def default_token_expiration_in_seconds(self) -> typing.Optional[jsii.Number]:
        '''The default token expiration in seconds for account linking.'''
        result = self._values.get("default_token_expiration_in_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def domains(self) -> typing.Optional[typing.List[builtins.str]]:
        '''An array of domains for account linking.'''
        result = self._values.get("domains")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def reciprocal_access_token_url(self) -> typing.Optional[builtins.str]:
        '''The reciprocal access token URL for account linking.'''
        result = self._values.get("reciprocal_access_token_url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def redirect_url(self) -> typing.Optional[typing.List[builtins.str]]:
        '''An array of redirect URLs for account linking.'''
        result = self._values.get("redirect_url")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def scopes(self) -> typing.Optional[typing.List[builtins.str]]:
        '''An array of scopes for account linking.'''
        result = self._values.get("scopes")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def skip_on_enablement(self) -> typing.Optional[builtins.bool]:
        '''Indicates whether to skip account linking on enablement.'''
        result = self._values.get("skip_on_enablement")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def voice_forward_account_linking(self) -> typing.Optional[builtins.str]:
        '''Voice-forward account linking setting, either 'ENABLED' or 'DISABLED'.'''
        result = self._values.get("voice_forward_account_linking")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AccountLinkingRequest(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AskCustomResource(
    _aws_cdk_ceddda9d.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-skill-management.AskCustomResource",
):
    '''A custom CloudFormation resource for Alexa Skill Kit SDK calls.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        on_create: typing.Optional[typing.Union["AskSdkCall", typing.Dict[builtins.str, typing.Any]]] = None,
        on_delete: typing.Optional[typing.Union["AskSdkCall", typing.Dict[builtins.str, typing.Any]]] = None,
        on_update: typing.Optional[typing.Union["AskSdkCall", typing.Dict[builtins.str, typing.Any]]] = None,
        removal_policy: typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy] = None,
        timeout: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        authentication_configuration: typing.Optional[typing.Union[_aws_cdk_alexa_ask_ceddda9d.CfnSkill.AuthenticationConfigurationProperty, typing.Dict[builtins.str, typing.Any]]] = None,
        authentication_configuration_parameter: typing.Optional[_aws_cdk_aws_ssm_ceddda9d.IStringParameter] = None,
        authentication_configuration_secret: typing.Optional[_aws_cdk_aws_secretsmanager_ceddda9d.ISecret] = None,
    ) -> None:
        '''Creates an instance of the Ask Custom Resource.

        :param scope: - The construct scope.
        :param id: - The construct ID.
        :param on_create: Action to perform on resource creation.
        :param on_delete: Action to perform on resource deletion.
        :param on_update: Action to perform on resource update.
        :param removal_policy: Removal policy for the custom resource.
        :param timeout: Timeout for the custom resource.
        :param authentication_configuration: Authentication configuration for the Alexa Skill.
        :param authentication_configuration_parameter: StringParameter holding the authentication configuration for the Alexa Skill.
        :param authentication_configuration_secret: Secret holding the authentication configuration for the Alexa Skill.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d43c356093f4b7cefaa23ce025ac0216fa0c9232f42bef5fd466f48595d7dddc)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = AskCustomResourceProps(
            on_create=on_create,
            on_delete=on_delete,
            on_update=on_update,
            removal_policy=removal_policy,
            timeout=timeout,
            authentication_configuration=authentication_configuration,
            authentication_configuration_parameter=authentication_configuration_parameter,
            authentication_configuration_secret=authentication_configuration_secret,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="getResponseField")
    def get_response_field(self, data_path: builtins.str) -> builtins.str:
        '''Gets the response field from the custom resource.

        :param data_path: - The data path to retrieve from the response.

        :return: The value of the response field.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b8d16c15b3ed43d105d5e1cd9c8e271ca33a03b139997f1b536fec196e34bbb0)
            check_type(argname="argument data_path", value=data_path, expected_type=type_hints["data_path"])
        return typing.cast(builtins.str, jsii.invoke(self, "getResponseField", [data_path]))


@jsii.data_type(
    jsii_type="cdk-skill-management.AskSdkCall",
    jsii_struct_bases=[],
    name_mapping={"action": "action", "parameters": "parameters"},
)
class AskSdkCall:
    def __init__(
        self,
        *,
        action: builtins.str,
        parameters: typing.Sequence[typing.Any],
    ) -> None:
        '''Represents a call to an ASK (Alexa Skill Kit) SDK service.

        :param action: The action or method to call in the ASK SDK service.
        :param parameters: An array of parameters to pass to the ASK SDK service call.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d2385967dc4bb6865f077cc56c802e9a316c9565ad392e3b0c7096a57eb62201)
            check_type(argname="argument action", value=action, expected_type=type_hints["action"])
            check_type(argname="argument parameters", value=parameters, expected_type=type_hints["parameters"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "action": action,
            "parameters": parameters,
        }

    @builtins.property
    def action(self) -> builtins.str:
        '''The action or method to call in the ASK SDK service.'''
        result = self._values.get("action")
        assert result is not None, "Required property 'action' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def parameters(self) -> typing.List[typing.Any]:
        '''An array of parameters to pass to the ASK SDK service call.'''
        result = self._values.get("parameters")
        assert result is not None, "Required property 'parameters' is missing"
        return typing.cast(typing.List[typing.Any], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AskSdkCall(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.interface(jsii_type="cdk-skill-management.IAccountLinking")
class IAccountLinking(_aws_cdk_ceddda9d.IResource, typing_extensions.Protocol):
    '''Interface representing an Account Linking resource.'''

    pass


class _IAccountLinkingProxy(
    jsii.proxy_for(_aws_cdk_ceddda9d.IResource), # type: ignore[misc]
):
    '''Interface representing an Account Linking resource.'''

    __jsii_type__: typing.ClassVar[str] = "cdk-skill-management.IAccountLinking"
    pass

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IAccountLinking).__jsii_proxy_class__ = lambda : _IAccountLinkingProxy


@jsii.interface(jsii_type="cdk-skill-management.ISkill")
class ISkill(_aws_cdk_ceddda9d.IResource, typing_extensions.Protocol):
    '''Interface representing an Alexa Skill.'''

    @builtins.property
    @jsii.member(jsii_name="skillId")
    def skill_id(self) -> builtins.str:
        '''The unique ID of the Alexa Skill.'''
        ...

    @builtins.property
    @jsii.member(jsii_name="skillStage")
    def skill_stage(self) -> builtins.str:
        '''The stage of the Alexa Skill.'''
        ...

    @builtins.property
    @jsii.member(jsii_name="skillType")
    def skill_type(self) -> "SkillType":
        '''The type of the Alexa Skill.'''
        ...


class _ISkillProxy(
    jsii.proxy_for(_aws_cdk_ceddda9d.IResource), # type: ignore[misc]
):
    '''Interface representing an Alexa Skill.'''

    __jsii_type__: typing.ClassVar[str] = "cdk-skill-management.ISkill"

    @builtins.property
    @jsii.member(jsii_name="skillId")
    def skill_id(self) -> builtins.str:
        '''The unique ID of the Alexa Skill.'''
        return typing.cast(builtins.str, jsii.get(self, "skillId"))

    @builtins.property
    @jsii.member(jsii_name="skillStage")
    def skill_stage(self) -> builtins.str:
        '''The stage of the Alexa Skill.'''
        return typing.cast(builtins.str, jsii.get(self, "skillStage"))

    @builtins.property
    @jsii.member(jsii_name="skillType")
    def skill_type(self) -> "SkillType":
        '''The type of the Alexa Skill.'''
        return typing.cast("SkillType", jsii.get(self, "skillType"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, ISkill).__jsii_proxy_class__ = lambda : _ISkillProxy


@jsii.interface(jsii_type="cdk-skill-management.ISkillEndpointPermission")
class ISkillEndpointPermission(typing_extensions.Protocol):
    '''Interface representing a Skill Endpoint Permission.'''

    @jsii.member(jsii_name="configureSkillId")
    def configure_skill_id(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        skill: ISkill,
    ) -> _constructs_77d1e7e8.IDependable:
        '''Configures a Skill Endpoint Permission for a specific skill.

        :param scope: - The construct scope.
        :param id: - The construct ID.
        :param skill: - The skill to configure the permission for.

        :return: An IDependable object representing the configured permission.
        '''
        ...


class _ISkillEndpointPermissionProxy:
    '''Interface representing a Skill Endpoint Permission.'''

    __jsii_type__: typing.ClassVar[str] = "cdk-skill-management.ISkillEndpointPermission"

    @jsii.member(jsii_name="configureSkillId")
    def configure_skill_id(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        skill: ISkill,
    ) -> _constructs_77d1e7e8.IDependable:
        '''Configures a Skill Endpoint Permission for a specific skill.

        :param scope: - The construct scope.
        :param id: - The construct ID.
        :param skill: - The skill to configure the permission for.

        :return: An IDependable object representing the configured permission.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d1442082a2d6739753cde107774c1ff3797d5e3c69cfae12226feb36e5ceb46c)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument skill", value=skill, expected_type=type_hints["skill"])
        return typing.cast(_constructs_77d1e7e8.IDependable, jsii.invoke(self, "configureSkillId", [scope, id, skill]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, ISkillEndpointPermission).__jsii_proxy_class__ = lambda : _ISkillEndpointPermissionProxy


@jsii.implements(ISkill)
class Skill(
    _aws_cdk_ceddda9d.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-skill-management.Skill",
):
    '''Alexa Skill construct for managing an Alexa Skill via CloudFormation.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        skill_package: typing.Union["SkillPackage", typing.Dict[builtins.str, typing.Any]],
        skill_stage: builtins.str,
        skill_type: "SkillType",
        vendor_id: builtins.str,
        authentication_configuration: typing.Optional[typing.Union[_aws_cdk_alexa_ask_ceddda9d.CfnSkill.AuthenticationConfigurationProperty, typing.Dict[builtins.str, typing.Any]]] = None,
        authentication_configuration_parameter: typing.Optional[_aws_cdk_aws_ssm_ceddda9d.IStringParameter] = None,
        authentication_configuration_secret: typing.Optional[_aws_cdk_aws_secretsmanager_ceddda9d.ISecret] = None,
    ) -> None:
        '''Creates an instance of the Alexa Skill construct.

        :param scope: - The construct scope.
        :param id: - The construct ID.
        :param skill_package: The package information for the Alexa Skill.
        :param skill_stage: The stage of the Alexa Skill.
        :param skill_type: The type of the Alexa Skill.
        :param vendor_id: The vendor ID of the Alexa Skill.
        :param authentication_configuration: Authentication configuration for the Alexa Skill.
        :param authentication_configuration_parameter: StringParameter holding the authentication configuration for the Alexa Skill.
        :param authentication_configuration_secret: Secret holding the authentication configuration for the Alexa Skill.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__df943b7d9b6ded55a4d694f44ce2d0b3045e85f6b48d4fa479e6afb508d7db28)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = SkillProps(
            skill_package=skill_package,
            skill_stage=skill_stage,
            skill_type=skill_type,
            vendor_id=vendor_id,
            authentication_configuration=authentication_configuration,
            authentication_configuration_parameter=authentication_configuration_parameter,
            authentication_configuration_secret=authentication_configuration_secret,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="fromAttributes")
    @builtins.classmethod
    def from_attributes(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        skill_id: builtins.str,
        skill_stage: builtins.str,
        skill_type: "SkillType",
    ) -> ISkill:
        '''Factory method to create an Alexa Skill from its attributes.

        :param scope: - The construct scope.
        :param id: - The construct ID.
        :param skill_id: The unique ID of the Alexa Skill.
        :param skill_stage: The stage of the Alexa Skill.
        :param skill_type: The type of the Alexa Skill.

        :return: The Alexa Skill construct.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e8bd80d800efb41600048bb5401f6f3531b3b6d65358e82671de7545ff19d7a)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        attributes = SkillAttributes(
            skill_id=skill_id, skill_stage=skill_stage, skill_type=skill_type
        )

        return typing.cast(ISkill, jsii.sinvoke(cls, "fromAttributes", [scope, id, attributes]))

    @jsii.member(jsii_name="fromSkillId")
    @builtins.classmethod
    def from_skill_id(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        skill_id: builtins.str,
    ) -> ISkill:
        '''Factory method to create an Alexa Skill from its ID.

        :param scope: - The construct scope.
        :param id: - The construct ID.
        :param skill_id: - The ID of the Alexa Skill.

        :return: The Alexa Skill construct.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__235486e5f2b971a7054153e2a6f140cf5629785fff502f8955add7f18bbdf8f9)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument skill_id", value=skill_id, expected_type=type_hints["skill_id"])
        return typing.cast(ISkill, jsii.sinvoke(cls, "fromSkillId", [scope, id, skill_id]))

    @builtins.property
    @jsii.member(jsii_name="skillId")
    def skill_id(self) -> builtins.str:
        '''The unique ID of the Alexa Skill.'''
        return typing.cast(builtins.str, jsii.get(self, "skillId"))

    @builtins.property
    @jsii.member(jsii_name="skillStage")
    def skill_stage(self) -> builtins.str:
        '''The stage of the Alexa Skill.'''
        return typing.cast(builtins.str, jsii.get(self, "skillStage"))

    @builtins.property
    @jsii.member(jsii_name="skillType")
    def skill_type(self) -> "SkillType":
        '''The type of the Alexa Skill.'''
        return typing.cast("SkillType", jsii.get(self, "skillType"))


@jsii.data_type(
    jsii_type="cdk-skill-management.SkillAttributes",
    jsii_struct_bases=[],
    name_mapping={
        "skill_id": "skillId",
        "skill_stage": "skillStage",
        "skill_type": "skillType",
    },
)
class SkillAttributes:
    def __init__(
        self,
        *,
        skill_id: builtins.str,
        skill_stage: builtins.str,
        skill_type: "SkillType",
    ) -> None:
        '''Properties for creating an Alexa Skill Instance from Attributes.

        :param skill_id: The unique ID of the Alexa Skill.
        :param skill_stage: The stage of the Alexa Skill.
        :param skill_type: The type of the Alexa Skill.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5216c5788c5ed42df78888d60975e65156e65b1aa125db9921854a72870bd985)
            check_type(argname="argument skill_id", value=skill_id, expected_type=type_hints["skill_id"])
            check_type(argname="argument skill_stage", value=skill_stage, expected_type=type_hints["skill_stage"])
            check_type(argname="argument skill_type", value=skill_type, expected_type=type_hints["skill_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "skill_id": skill_id,
            "skill_stage": skill_stage,
            "skill_type": skill_type,
        }

    @builtins.property
    def skill_id(self) -> builtins.str:
        '''The unique ID of the Alexa Skill.'''
        result = self._values.get("skill_id")
        assert result is not None, "Required property 'skill_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def skill_stage(self) -> builtins.str:
        '''The stage of the Alexa Skill.'''
        result = self._values.get("skill_stage")
        assert result is not None, "Required property 'skill_stage' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def skill_type(self) -> "SkillType":
        '''The type of the Alexa Skill.'''
        result = self._values.get("skill_type")
        assert result is not None, "Required property 'skill_type' is missing"
        return typing.cast("SkillType", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SkillAttributes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-skill-management.SkillAuthenticationProps",
    jsii_struct_bases=[],
    name_mapping={
        "authentication_configuration": "authenticationConfiguration",
        "authentication_configuration_parameter": "authenticationConfigurationParameter",
        "authentication_configuration_secret": "authenticationConfigurationSecret",
    },
)
class SkillAuthenticationProps:
    def __init__(
        self,
        *,
        authentication_configuration: typing.Optional[typing.Union[_aws_cdk_alexa_ask_ceddda9d.CfnSkill.AuthenticationConfigurationProperty, typing.Dict[builtins.str, typing.Any]]] = None,
        authentication_configuration_parameter: typing.Optional[_aws_cdk_aws_ssm_ceddda9d.IStringParameter] = None,
        authentication_configuration_secret: typing.Optional[_aws_cdk_aws_secretsmanager_ceddda9d.ISecret] = None,
    ) -> None:
        '''Properties for configuring the authentication properties for Skill Management.

        :param authentication_configuration: Authentication configuration for the Alexa Skill.
        :param authentication_configuration_parameter: StringParameter holding the authentication configuration for the Alexa Skill.
        :param authentication_configuration_secret: Secret holding the authentication configuration for the Alexa Skill.
        '''
        if isinstance(authentication_configuration, dict):
            authentication_configuration = _aws_cdk_alexa_ask_ceddda9d.CfnSkill.AuthenticationConfigurationProperty(**authentication_configuration)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__70f3155eee97687129f34335a8b0742ca7719f07b9a86186177bb18dac389a71)
            check_type(argname="argument authentication_configuration", value=authentication_configuration, expected_type=type_hints["authentication_configuration"])
            check_type(argname="argument authentication_configuration_parameter", value=authentication_configuration_parameter, expected_type=type_hints["authentication_configuration_parameter"])
            check_type(argname="argument authentication_configuration_secret", value=authentication_configuration_secret, expected_type=type_hints["authentication_configuration_secret"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if authentication_configuration is not None:
            self._values["authentication_configuration"] = authentication_configuration
        if authentication_configuration_parameter is not None:
            self._values["authentication_configuration_parameter"] = authentication_configuration_parameter
        if authentication_configuration_secret is not None:
            self._values["authentication_configuration_secret"] = authentication_configuration_secret

    @builtins.property
    def authentication_configuration(
        self,
    ) -> typing.Optional[_aws_cdk_alexa_ask_ceddda9d.CfnSkill.AuthenticationConfigurationProperty]:
        '''Authentication configuration for the Alexa Skill.'''
        result = self._values.get("authentication_configuration")
        return typing.cast(typing.Optional[_aws_cdk_alexa_ask_ceddda9d.CfnSkill.AuthenticationConfigurationProperty], result)

    @builtins.property
    def authentication_configuration_parameter(
        self,
    ) -> typing.Optional[_aws_cdk_aws_ssm_ceddda9d.IStringParameter]:
        '''StringParameter holding the authentication configuration for the Alexa Skill.'''
        result = self._values.get("authentication_configuration_parameter")
        return typing.cast(typing.Optional[_aws_cdk_aws_ssm_ceddda9d.IStringParameter], result)

    @builtins.property
    def authentication_configuration_secret(
        self,
    ) -> typing.Optional[_aws_cdk_aws_secretsmanager_ceddda9d.ISecret]:
        '''Secret holding the authentication configuration for the Alexa Skill.'''
        result = self._values.get("authentication_configuration_secret")
        return typing.cast(typing.Optional[_aws_cdk_aws_secretsmanager_ceddda9d.ISecret], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SkillAuthenticationProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(ISkillEndpointPermission)
class SkillEndpointPermission(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-skill-management.SkillEndpointPermission",
):
    '''Class for configuring and managing Skill Endpoint Permissions.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        handler: _aws_cdk_aws_lambda_ceddda9d.IFunction,
        skill_type: "SkillType",
    ) -> None:
        '''Creates an instance of the Skill Endpoint Permission.

        :param scope: - The construct scope.
        :param id: - The construct ID.
        :param handler: The AWS Lambda function handler to configure the permission for.
        :param skill_type: The Type of the Skill, which will be created later.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2556f73f8e7c732aeec5a54979ba717e03bea8ac030317775cd2e17e07cb2a6c)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = SkillEndpointProps(handler=handler, skill_type=skill_type)

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="configureSkillId")
    def configure_skill_id(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        skill: ISkill,
    ) -> _constructs_77d1e7e8.IDependable:
        '''Configures a Skill Endpoint Permission for a specific skill.

        This replaces the initially created permission with a new permission checking for the SkillId.

        :param scope: - The construct scope.
        :param id: - The construct ID.
        :param skill: - The skill to configure the permission for.

        :return: An IDependable object representing the configured permission.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eefe0a533c7536afbc152ffdbcd2c35a55520d5ee2126618005b1536a5456742)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument skill", value=skill, expected_type=type_hints["skill"])
        return typing.cast(_constructs_77d1e7e8.IDependable, jsii.invoke(self, "configureSkillId", [scope, id, skill]))


@jsii.data_type(
    jsii_type="cdk-skill-management.SkillEndpointProps",
    jsii_struct_bases=[],
    name_mapping={"handler": "handler", "skill_type": "skillType"},
)
class SkillEndpointProps:
    def __init__(
        self,
        *,
        handler: _aws_cdk_aws_lambda_ceddda9d.IFunction,
        skill_type: "SkillType",
    ) -> None:
        '''Properties for configuring a Skill Endpoint Permission.

        :param handler: The AWS Lambda function handler to configure the permission for.
        :param skill_type: The Type of the Skill, which will be created later.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e6158f68c59cc895e3c48c715845928605c34d79a926860075b01d66afcab56)
            check_type(argname="argument handler", value=handler, expected_type=type_hints["handler"])
            check_type(argname="argument skill_type", value=skill_type, expected_type=type_hints["skill_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "handler": handler,
            "skill_type": skill_type,
        }

    @builtins.property
    def handler(self) -> _aws_cdk_aws_lambda_ceddda9d.IFunction:
        '''The AWS Lambda function handler to configure the permission for.'''
        result = self._values.get("handler")
        assert result is not None, "Required property 'handler' is missing"
        return typing.cast(_aws_cdk_aws_lambda_ceddda9d.IFunction, result)

    @builtins.property
    def skill_type(self) -> "SkillType":
        '''The Type of the Skill, which will be created later.'''
        result = self._values.get("skill_type")
        assert result is not None, "Required property 'skill_type' is missing"
        return typing.cast("SkillType", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SkillEndpointProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-skill-management.SkillPackage",
    jsii_struct_bases=[],
    name_mapping={"asset": "asset", "overrides": "overrides"},
)
class SkillPackage:
    def __init__(
        self,
        *,
        asset: _aws_cdk_aws_s3_assets_ceddda9d.Asset,
        overrides: typing.Optional[typing.Union[_aws_cdk_alexa_ask_ceddda9d.CfnSkill.OverridesProperty, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''Interface representing an Alexa Skill package.

        :param asset: The asset associated with the Alexa Skill package.
        :param overrides: Overrides for the Alexa Skill package.
        '''
        if isinstance(overrides, dict):
            overrides = _aws_cdk_alexa_ask_ceddda9d.CfnSkill.OverridesProperty(**overrides)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b8e9f54c7f7bef80e827bf8176bd19e70aff16ce7eab6e2b9a50dee7187b9db7)
            check_type(argname="argument asset", value=asset, expected_type=type_hints["asset"])
            check_type(argname="argument overrides", value=overrides, expected_type=type_hints["overrides"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "asset": asset,
        }
        if overrides is not None:
            self._values["overrides"] = overrides

    @builtins.property
    def asset(self) -> _aws_cdk_aws_s3_assets_ceddda9d.Asset:
        '''The asset associated with the Alexa Skill package.'''
        result = self._values.get("asset")
        assert result is not None, "Required property 'asset' is missing"
        return typing.cast(_aws_cdk_aws_s3_assets_ceddda9d.Asset, result)

    @builtins.property
    def overrides(
        self,
    ) -> typing.Optional[_aws_cdk_alexa_ask_ceddda9d.CfnSkill.OverridesProperty]:
        '''Overrides for the Alexa Skill package.'''
        result = self._values.get("overrides")
        return typing.cast(typing.Optional[_aws_cdk_alexa_ask_ceddda9d.CfnSkill.OverridesProperty], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SkillPackage(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-skill-management.SkillProps",
    jsii_struct_bases=[SkillAuthenticationProps],
    name_mapping={
        "authentication_configuration": "authenticationConfiguration",
        "authentication_configuration_parameter": "authenticationConfigurationParameter",
        "authentication_configuration_secret": "authenticationConfigurationSecret",
        "skill_package": "skillPackage",
        "skill_stage": "skillStage",
        "skill_type": "skillType",
        "vendor_id": "vendorId",
    },
)
class SkillProps(SkillAuthenticationProps):
    def __init__(
        self,
        *,
        authentication_configuration: typing.Optional[typing.Union[_aws_cdk_alexa_ask_ceddda9d.CfnSkill.AuthenticationConfigurationProperty, typing.Dict[builtins.str, typing.Any]]] = None,
        authentication_configuration_parameter: typing.Optional[_aws_cdk_aws_ssm_ceddda9d.IStringParameter] = None,
        authentication_configuration_secret: typing.Optional[_aws_cdk_aws_secretsmanager_ceddda9d.ISecret] = None,
        skill_package: typing.Union[SkillPackage, typing.Dict[builtins.str, typing.Any]],
        skill_stage: builtins.str,
        skill_type: "SkillType",
        vendor_id: builtins.str,
    ) -> None:
        '''Properties for creating an Alexa Skill.

        :param authentication_configuration: Authentication configuration for the Alexa Skill.
        :param authentication_configuration_parameter: StringParameter holding the authentication configuration for the Alexa Skill.
        :param authentication_configuration_secret: Secret holding the authentication configuration for the Alexa Skill.
        :param skill_package: The package information for the Alexa Skill.
        :param skill_stage: The stage of the Alexa Skill.
        :param skill_type: The type of the Alexa Skill.
        :param vendor_id: The vendor ID of the Alexa Skill.
        '''
        if isinstance(authentication_configuration, dict):
            authentication_configuration = _aws_cdk_alexa_ask_ceddda9d.CfnSkill.AuthenticationConfigurationProperty(**authentication_configuration)
        if isinstance(skill_package, dict):
            skill_package = SkillPackage(**skill_package)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd5814d7741914291e2779f4fa43f4ae6dfe5f720f5e1231c7e962cd568b949c)
            check_type(argname="argument authentication_configuration", value=authentication_configuration, expected_type=type_hints["authentication_configuration"])
            check_type(argname="argument authentication_configuration_parameter", value=authentication_configuration_parameter, expected_type=type_hints["authentication_configuration_parameter"])
            check_type(argname="argument authentication_configuration_secret", value=authentication_configuration_secret, expected_type=type_hints["authentication_configuration_secret"])
            check_type(argname="argument skill_package", value=skill_package, expected_type=type_hints["skill_package"])
            check_type(argname="argument skill_stage", value=skill_stage, expected_type=type_hints["skill_stage"])
            check_type(argname="argument skill_type", value=skill_type, expected_type=type_hints["skill_type"])
            check_type(argname="argument vendor_id", value=vendor_id, expected_type=type_hints["vendor_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "skill_package": skill_package,
            "skill_stage": skill_stage,
            "skill_type": skill_type,
            "vendor_id": vendor_id,
        }
        if authentication_configuration is not None:
            self._values["authentication_configuration"] = authentication_configuration
        if authentication_configuration_parameter is not None:
            self._values["authentication_configuration_parameter"] = authentication_configuration_parameter
        if authentication_configuration_secret is not None:
            self._values["authentication_configuration_secret"] = authentication_configuration_secret

    @builtins.property
    def authentication_configuration(
        self,
    ) -> typing.Optional[_aws_cdk_alexa_ask_ceddda9d.CfnSkill.AuthenticationConfigurationProperty]:
        '''Authentication configuration for the Alexa Skill.'''
        result = self._values.get("authentication_configuration")
        return typing.cast(typing.Optional[_aws_cdk_alexa_ask_ceddda9d.CfnSkill.AuthenticationConfigurationProperty], result)

    @builtins.property
    def authentication_configuration_parameter(
        self,
    ) -> typing.Optional[_aws_cdk_aws_ssm_ceddda9d.IStringParameter]:
        '''StringParameter holding the authentication configuration for the Alexa Skill.'''
        result = self._values.get("authentication_configuration_parameter")
        return typing.cast(typing.Optional[_aws_cdk_aws_ssm_ceddda9d.IStringParameter], result)

    @builtins.property
    def authentication_configuration_secret(
        self,
    ) -> typing.Optional[_aws_cdk_aws_secretsmanager_ceddda9d.ISecret]:
        '''Secret holding the authentication configuration for the Alexa Skill.'''
        result = self._values.get("authentication_configuration_secret")
        return typing.cast(typing.Optional[_aws_cdk_aws_secretsmanager_ceddda9d.ISecret], result)

    @builtins.property
    def skill_package(self) -> SkillPackage:
        '''The package information for the Alexa Skill.'''
        result = self._values.get("skill_package")
        assert result is not None, "Required property 'skill_package' is missing"
        return typing.cast(SkillPackage, result)

    @builtins.property
    def skill_stage(self) -> builtins.str:
        '''The stage of the Alexa Skill.'''
        result = self._values.get("skill_stage")
        assert result is not None, "Required property 'skill_stage' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def skill_type(self) -> "SkillType":
        '''The type of the Alexa Skill.'''
        result = self._values.get("skill_type")
        assert result is not None, "Required property 'skill_type' is missing"
        return typing.cast("SkillType", result)

    @builtins.property
    def vendor_id(self) -> builtins.str:
        '''The vendor ID of the Alexa Skill.'''
        result = self._values.get("vendor_id")
        assert result is not None, "Required property 'vendor_id' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SkillProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="cdk-skill-management.SkillType")
class SkillType(enum.Enum):
    '''Enumeration for different Alexa Skill types.'''

    CUSTOM = "CUSTOM"
    SMART_HOME = "SMART_HOME"


@jsii.implements(IAccountLinking)
class AccountLinking(
    _aws_cdk_ceddda9d.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-skill-management.AccountLinking",
):
    '''Represents an Account Linking resource for an Alexa Skill.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        request: typing.Union[AccountLinkingRequest, typing.Dict[builtins.str, typing.Any]],
        skill: ISkill,
        authentication_configuration: typing.Optional[typing.Union[_aws_cdk_alexa_ask_ceddda9d.CfnSkill.AuthenticationConfigurationProperty, typing.Dict[builtins.str, typing.Any]]] = None,
        authentication_configuration_parameter: typing.Optional[_aws_cdk_aws_ssm_ceddda9d.IStringParameter] = None,
        authentication_configuration_secret: typing.Optional[_aws_cdk_aws_secretsmanager_ceddda9d.ISecret] = None,
    ) -> None:
        '''Creates an instance of the Account Linking resource.

        :param scope: - The construct scope.
        :param id: - The construct ID.
        :param request: The request parameters for account linking.
        :param skill: The Alexa Skill for which account linking is configured.
        :param authentication_configuration: Authentication configuration for the Alexa Skill.
        :param authentication_configuration_parameter: StringParameter holding the authentication configuration for the Alexa Skill.
        :param authentication_configuration_secret: Secret holding the authentication configuration for the Alexa Skill.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f777726294473cbc9901c273f080ef4db899c5d7db9684576a71128e1b28b7f)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = AccountLinkingProps(
            request=request,
            skill=skill,
            authentication_configuration=authentication_configuration,
            authentication_configuration_parameter=authentication_configuration_parameter,
            authentication_configuration_secret=authentication_configuration_secret,
        )

        jsii.create(self.__class__, self, [scope, id, props])


@jsii.data_type(
    jsii_type="cdk-skill-management.AccountLinkingProps",
    jsii_struct_bases=[SkillAuthenticationProps],
    name_mapping={
        "authentication_configuration": "authenticationConfiguration",
        "authentication_configuration_parameter": "authenticationConfigurationParameter",
        "authentication_configuration_secret": "authenticationConfigurationSecret",
        "request": "request",
        "skill": "skill",
    },
)
class AccountLinkingProps(SkillAuthenticationProps):
    def __init__(
        self,
        *,
        authentication_configuration: typing.Optional[typing.Union[_aws_cdk_alexa_ask_ceddda9d.CfnSkill.AuthenticationConfigurationProperty, typing.Dict[builtins.str, typing.Any]]] = None,
        authentication_configuration_parameter: typing.Optional[_aws_cdk_aws_ssm_ceddda9d.IStringParameter] = None,
        authentication_configuration_secret: typing.Optional[_aws_cdk_aws_secretsmanager_ceddda9d.ISecret] = None,
        request: typing.Union[AccountLinkingRequest, typing.Dict[builtins.str, typing.Any]],
        skill: ISkill,
    ) -> None:
        '''Properties for creating an Account Linking resource.

        :param authentication_configuration: Authentication configuration for the Alexa Skill.
        :param authentication_configuration_parameter: StringParameter holding the authentication configuration for the Alexa Skill.
        :param authentication_configuration_secret: Secret holding the authentication configuration for the Alexa Skill.
        :param request: The request parameters for account linking.
        :param skill: The Alexa Skill for which account linking is configured.
        '''
        if isinstance(authentication_configuration, dict):
            authentication_configuration = _aws_cdk_alexa_ask_ceddda9d.CfnSkill.AuthenticationConfigurationProperty(**authentication_configuration)
        if isinstance(request, dict):
            request = AccountLinkingRequest(**request)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f563ced17f0659a4108b2b8af1c27b0231c4a3c3c0d4caeffe2a400e38e9ae6)
            check_type(argname="argument authentication_configuration", value=authentication_configuration, expected_type=type_hints["authentication_configuration"])
            check_type(argname="argument authentication_configuration_parameter", value=authentication_configuration_parameter, expected_type=type_hints["authentication_configuration_parameter"])
            check_type(argname="argument authentication_configuration_secret", value=authentication_configuration_secret, expected_type=type_hints["authentication_configuration_secret"])
            check_type(argname="argument request", value=request, expected_type=type_hints["request"])
            check_type(argname="argument skill", value=skill, expected_type=type_hints["skill"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "request": request,
            "skill": skill,
        }
        if authentication_configuration is not None:
            self._values["authentication_configuration"] = authentication_configuration
        if authentication_configuration_parameter is not None:
            self._values["authentication_configuration_parameter"] = authentication_configuration_parameter
        if authentication_configuration_secret is not None:
            self._values["authentication_configuration_secret"] = authentication_configuration_secret

    @builtins.property
    def authentication_configuration(
        self,
    ) -> typing.Optional[_aws_cdk_alexa_ask_ceddda9d.CfnSkill.AuthenticationConfigurationProperty]:
        '''Authentication configuration for the Alexa Skill.'''
        result = self._values.get("authentication_configuration")
        return typing.cast(typing.Optional[_aws_cdk_alexa_ask_ceddda9d.CfnSkill.AuthenticationConfigurationProperty], result)

    @builtins.property
    def authentication_configuration_parameter(
        self,
    ) -> typing.Optional[_aws_cdk_aws_ssm_ceddda9d.IStringParameter]:
        '''StringParameter holding the authentication configuration for the Alexa Skill.'''
        result = self._values.get("authentication_configuration_parameter")
        return typing.cast(typing.Optional[_aws_cdk_aws_ssm_ceddda9d.IStringParameter], result)

    @builtins.property
    def authentication_configuration_secret(
        self,
    ) -> typing.Optional[_aws_cdk_aws_secretsmanager_ceddda9d.ISecret]:
        '''Secret holding the authentication configuration for the Alexa Skill.'''
        result = self._values.get("authentication_configuration_secret")
        return typing.cast(typing.Optional[_aws_cdk_aws_secretsmanager_ceddda9d.ISecret], result)

    @builtins.property
    def request(self) -> AccountLinkingRequest:
        '''The request parameters for account linking.'''
        result = self._values.get("request")
        assert result is not None, "Required property 'request' is missing"
        return typing.cast(AccountLinkingRequest, result)

    @builtins.property
    def skill(self) -> ISkill:
        '''The Alexa Skill for which account linking is configured.'''
        result = self._values.get("skill")
        assert result is not None, "Required property 'skill' is missing"
        return typing.cast(ISkill, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AccountLinkingProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-skill-management.AskCustomResourceProps",
    jsii_struct_bases=[SkillAuthenticationProps],
    name_mapping={
        "authentication_configuration": "authenticationConfiguration",
        "authentication_configuration_parameter": "authenticationConfigurationParameter",
        "authentication_configuration_secret": "authenticationConfigurationSecret",
        "on_create": "onCreate",
        "on_delete": "onDelete",
        "on_update": "onUpdate",
        "removal_policy": "removalPolicy",
        "timeout": "timeout",
    },
)
class AskCustomResourceProps(SkillAuthenticationProps):
    def __init__(
        self,
        *,
        authentication_configuration: typing.Optional[typing.Union[_aws_cdk_alexa_ask_ceddda9d.CfnSkill.AuthenticationConfigurationProperty, typing.Dict[builtins.str, typing.Any]]] = None,
        authentication_configuration_parameter: typing.Optional[_aws_cdk_aws_ssm_ceddda9d.IStringParameter] = None,
        authentication_configuration_secret: typing.Optional[_aws_cdk_aws_secretsmanager_ceddda9d.ISecret] = None,
        on_create: typing.Optional[typing.Union[AskSdkCall, typing.Dict[builtins.str, typing.Any]]] = None,
        on_delete: typing.Optional[typing.Union[AskSdkCall, typing.Dict[builtins.str, typing.Any]]] = None,
        on_update: typing.Optional[typing.Union[AskSdkCall, typing.Dict[builtins.str, typing.Any]]] = None,
        removal_policy: typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy] = None,
        timeout: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    ) -> None:
        '''Properties for configuring an Ask Custom Resource.

        :param authentication_configuration: Authentication configuration for the Alexa Skill.
        :param authentication_configuration_parameter: StringParameter holding the authentication configuration for the Alexa Skill.
        :param authentication_configuration_secret: Secret holding the authentication configuration for the Alexa Skill.
        :param on_create: Action to perform on resource creation.
        :param on_delete: Action to perform on resource deletion.
        :param on_update: Action to perform on resource update.
        :param removal_policy: Removal policy for the custom resource.
        :param timeout: Timeout for the custom resource.
        '''
        if isinstance(authentication_configuration, dict):
            authentication_configuration = _aws_cdk_alexa_ask_ceddda9d.CfnSkill.AuthenticationConfigurationProperty(**authentication_configuration)
        if isinstance(on_create, dict):
            on_create = AskSdkCall(**on_create)
        if isinstance(on_delete, dict):
            on_delete = AskSdkCall(**on_delete)
        if isinstance(on_update, dict):
            on_update = AskSdkCall(**on_update)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f998c085541c113747ccbafdb6f77fb421c340c085f031d67efbb806ac94cae)
            check_type(argname="argument authentication_configuration", value=authentication_configuration, expected_type=type_hints["authentication_configuration"])
            check_type(argname="argument authentication_configuration_parameter", value=authentication_configuration_parameter, expected_type=type_hints["authentication_configuration_parameter"])
            check_type(argname="argument authentication_configuration_secret", value=authentication_configuration_secret, expected_type=type_hints["authentication_configuration_secret"])
            check_type(argname="argument on_create", value=on_create, expected_type=type_hints["on_create"])
            check_type(argname="argument on_delete", value=on_delete, expected_type=type_hints["on_delete"])
            check_type(argname="argument on_update", value=on_update, expected_type=type_hints["on_update"])
            check_type(argname="argument removal_policy", value=removal_policy, expected_type=type_hints["removal_policy"])
            check_type(argname="argument timeout", value=timeout, expected_type=type_hints["timeout"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if authentication_configuration is not None:
            self._values["authentication_configuration"] = authentication_configuration
        if authentication_configuration_parameter is not None:
            self._values["authentication_configuration_parameter"] = authentication_configuration_parameter
        if authentication_configuration_secret is not None:
            self._values["authentication_configuration_secret"] = authentication_configuration_secret
        if on_create is not None:
            self._values["on_create"] = on_create
        if on_delete is not None:
            self._values["on_delete"] = on_delete
        if on_update is not None:
            self._values["on_update"] = on_update
        if removal_policy is not None:
            self._values["removal_policy"] = removal_policy
        if timeout is not None:
            self._values["timeout"] = timeout

    @builtins.property
    def authentication_configuration(
        self,
    ) -> typing.Optional[_aws_cdk_alexa_ask_ceddda9d.CfnSkill.AuthenticationConfigurationProperty]:
        '''Authentication configuration for the Alexa Skill.'''
        result = self._values.get("authentication_configuration")
        return typing.cast(typing.Optional[_aws_cdk_alexa_ask_ceddda9d.CfnSkill.AuthenticationConfigurationProperty], result)

    @builtins.property
    def authentication_configuration_parameter(
        self,
    ) -> typing.Optional[_aws_cdk_aws_ssm_ceddda9d.IStringParameter]:
        '''StringParameter holding the authentication configuration for the Alexa Skill.'''
        result = self._values.get("authentication_configuration_parameter")
        return typing.cast(typing.Optional[_aws_cdk_aws_ssm_ceddda9d.IStringParameter], result)

    @builtins.property
    def authentication_configuration_secret(
        self,
    ) -> typing.Optional[_aws_cdk_aws_secretsmanager_ceddda9d.ISecret]:
        '''Secret holding the authentication configuration for the Alexa Skill.'''
        result = self._values.get("authentication_configuration_secret")
        return typing.cast(typing.Optional[_aws_cdk_aws_secretsmanager_ceddda9d.ISecret], result)

    @builtins.property
    def on_create(self) -> typing.Optional[AskSdkCall]:
        '''Action to perform on resource creation.'''
        result = self._values.get("on_create")
        return typing.cast(typing.Optional[AskSdkCall], result)

    @builtins.property
    def on_delete(self) -> typing.Optional[AskSdkCall]:
        '''Action to perform on resource deletion.'''
        result = self._values.get("on_delete")
        return typing.cast(typing.Optional[AskSdkCall], result)

    @builtins.property
    def on_update(self) -> typing.Optional[AskSdkCall]:
        '''Action to perform on resource update.'''
        result = self._values.get("on_update")
        return typing.cast(typing.Optional[AskSdkCall], result)

    @builtins.property
    def removal_policy(self) -> typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy]:
        '''Removal policy for the custom resource.'''
        result = self._values.get("removal_policy")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy], result)

    @builtins.property
    def timeout(self) -> typing.Optional[_aws_cdk_ceddda9d.Duration]:
        '''Timeout for the custom resource.'''
        result = self._values.get("timeout")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.Duration], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AskCustomResourceProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "AccountLinking",
    "AccountLinkingPlatformAuthorizationUrl",
    "AccountLinkingProps",
    "AccountLinkingRequest",
    "AskCustomResource",
    "AskCustomResourceProps",
    "AskSdkCall",
    "IAccountLinking",
    "ISkill",
    "ISkillEndpointPermission",
    "Skill",
    "SkillAttributes",
    "SkillAuthenticationProps",
    "SkillEndpointPermission",
    "SkillEndpointProps",
    "SkillPackage",
    "SkillProps",
    "SkillType",
]

publication.publish()

def _typecheckingstub__6f884dc6d966eaaf535502a58835af4763a09088c8d530d6338e96ed080db5ff(
    *,
    platform_authorization_url: builtins.str,
    platform_type: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6ec99be4a6947103f12e33db65670189692f73c3aa14e510a48a2e4d30598d9(
    *,
    access_token_scheme: typing.Optional[builtins.str] = None,
    access_token_url: typing.Optional[builtins.str] = None,
    authentication_flow_type: typing.Optional[builtins.str] = None,
    authorization_url: typing.Optional[builtins.str] = None,
    authorization_urls_by_platform: typing.Optional[typing.Sequence[typing.Union[AccountLinkingPlatformAuthorizationUrl, typing.Dict[builtins.str, typing.Any]]]] = None,
    client_id: typing.Optional[builtins.str] = None,
    client_secret: typing.Optional[builtins.str] = None,
    default_token_expiration_in_seconds: typing.Optional[jsii.Number] = None,
    domains: typing.Optional[typing.Sequence[builtins.str]] = None,
    reciprocal_access_token_url: typing.Optional[builtins.str] = None,
    redirect_url: typing.Optional[typing.Sequence[builtins.str]] = None,
    scopes: typing.Optional[typing.Sequence[builtins.str]] = None,
    skip_on_enablement: typing.Optional[builtins.bool] = None,
    voice_forward_account_linking: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d43c356093f4b7cefaa23ce025ac0216fa0c9232f42bef5fd466f48595d7dddc(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    on_create: typing.Optional[typing.Union[AskSdkCall, typing.Dict[builtins.str, typing.Any]]] = None,
    on_delete: typing.Optional[typing.Union[AskSdkCall, typing.Dict[builtins.str, typing.Any]]] = None,
    on_update: typing.Optional[typing.Union[AskSdkCall, typing.Dict[builtins.str, typing.Any]]] = None,
    removal_policy: typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy] = None,
    timeout: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    authentication_configuration: typing.Optional[typing.Union[_aws_cdk_alexa_ask_ceddda9d.CfnSkill.AuthenticationConfigurationProperty, typing.Dict[builtins.str, typing.Any]]] = None,
    authentication_configuration_parameter: typing.Optional[_aws_cdk_aws_ssm_ceddda9d.IStringParameter] = None,
    authentication_configuration_secret: typing.Optional[_aws_cdk_aws_secretsmanager_ceddda9d.ISecret] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8d16c15b3ed43d105d5e1cd9c8e271ca33a03b139997f1b536fec196e34bbb0(
    data_path: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2385967dc4bb6865f077cc56c802e9a316c9565ad392e3b0c7096a57eb62201(
    *,
    action: builtins.str,
    parameters: typing.Sequence[typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1442082a2d6739753cde107774c1ff3797d5e3c69cfae12226feb36e5ceb46c(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    skill: ISkill,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df943b7d9b6ded55a4d694f44ce2d0b3045e85f6b48d4fa479e6afb508d7db28(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    skill_package: typing.Union[SkillPackage, typing.Dict[builtins.str, typing.Any]],
    skill_stage: builtins.str,
    skill_type: SkillType,
    vendor_id: builtins.str,
    authentication_configuration: typing.Optional[typing.Union[_aws_cdk_alexa_ask_ceddda9d.CfnSkill.AuthenticationConfigurationProperty, typing.Dict[builtins.str, typing.Any]]] = None,
    authentication_configuration_parameter: typing.Optional[_aws_cdk_aws_ssm_ceddda9d.IStringParameter] = None,
    authentication_configuration_secret: typing.Optional[_aws_cdk_aws_secretsmanager_ceddda9d.ISecret] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e8bd80d800efb41600048bb5401f6f3531b3b6d65358e82671de7545ff19d7a(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    skill_id: builtins.str,
    skill_stage: builtins.str,
    skill_type: SkillType,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__235486e5f2b971a7054153e2a6f140cf5629785fff502f8955add7f18bbdf8f9(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    skill_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5216c5788c5ed42df78888d60975e65156e65b1aa125db9921854a72870bd985(
    *,
    skill_id: builtins.str,
    skill_stage: builtins.str,
    skill_type: SkillType,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70f3155eee97687129f34335a8b0742ca7719f07b9a86186177bb18dac389a71(
    *,
    authentication_configuration: typing.Optional[typing.Union[_aws_cdk_alexa_ask_ceddda9d.CfnSkill.AuthenticationConfigurationProperty, typing.Dict[builtins.str, typing.Any]]] = None,
    authentication_configuration_parameter: typing.Optional[_aws_cdk_aws_ssm_ceddda9d.IStringParameter] = None,
    authentication_configuration_secret: typing.Optional[_aws_cdk_aws_secretsmanager_ceddda9d.ISecret] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2556f73f8e7c732aeec5a54979ba717e03bea8ac030317775cd2e17e07cb2a6c(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    handler: _aws_cdk_aws_lambda_ceddda9d.IFunction,
    skill_type: SkillType,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eefe0a533c7536afbc152ffdbcd2c35a55520d5ee2126618005b1536a5456742(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    skill: ISkill,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e6158f68c59cc895e3c48c715845928605c34d79a926860075b01d66afcab56(
    *,
    handler: _aws_cdk_aws_lambda_ceddda9d.IFunction,
    skill_type: SkillType,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8e9f54c7f7bef80e827bf8176bd19e70aff16ce7eab6e2b9a50dee7187b9db7(
    *,
    asset: _aws_cdk_aws_s3_assets_ceddda9d.Asset,
    overrides: typing.Optional[typing.Union[_aws_cdk_alexa_ask_ceddda9d.CfnSkill.OverridesProperty, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd5814d7741914291e2779f4fa43f4ae6dfe5f720f5e1231c7e962cd568b949c(
    *,
    authentication_configuration: typing.Optional[typing.Union[_aws_cdk_alexa_ask_ceddda9d.CfnSkill.AuthenticationConfigurationProperty, typing.Dict[builtins.str, typing.Any]]] = None,
    authentication_configuration_parameter: typing.Optional[_aws_cdk_aws_ssm_ceddda9d.IStringParameter] = None,
    authentication_configuration_secret: typing.Optional[_aws_cdk_aws_secretsmanager_ceddda9d.ISecret] = None,
    skill_package: typing.Union[SkillPackage, typing.Dict[builtins.str, typing.Any]],
    skill_stage: builtins.str,
    skill_type: SkillType,
    vendor_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f777726294473cbc9901c273f080ef4db899c5d7db9684576a71128e1b28b7f(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    request: typing.Union[AccountLinkingRequest, typing.Dict[builtins.str, typing.Any]],
    skill: ISkill,
    authentication_configuration: typing.Optional[typing.Union[_aws_cdk_alexa_ask_ceddda9d.CfnSkill.AuthenticationConfigurationProperty, typing.Dict[builtins.str, typing.Any]]] = None,
    authentication_configuration_parameter: typing.Optional[_aws_cdk_aws_ssm_ceddda9d.IStringParameter] = None,
    authentication_configuration_secret: typing.Optional[_aws_cdk_aws_secretsmanager_ceddda9d.ISecret] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f563ced17f0659a4108b2b8af1c27b0231c4a3c3c0d4caeffe2a400e38e9ae6(
    *,
    authentication_configuration: typing.Optional[typing.Union[_aws_cdk_alexa_ask_ceddda9d.CfnSkill.AuthenticationConfigurationProperty, typing.Dict[builtins.str, typing.Any]]] = None,
    authentication_configuration_parameter: typing.Optional[_aws_cdk_aws_ssm_ceddda9d.IStringParameter] = None,
    authentication_configuration_secret: typing.Optional[_aws_cdk_aws_secretsmanager_ceddda9d.ISecret] = None,
    request: typing.Union[AccountLinkingRequest, typing.Dict[builtins.str, typing.Any]],
    skill: ISkill,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f998c085541c113747ccbafdb6f77fb421c340c085f031d67efbb806ac94cae(
    *,
    authentication_configuration: typing.Optional[typing.Union[_aws_cdk_alexa_ask_ceddda9d.CfnSkill.AuthenticationConfigurationProperty, typing.Dict[builtins.str, typing.Any]]] = None,
    authentication_configuration_parameter: typing.Optional[_aws_cdk_aws_ssm_ceddda9d.IStringParameter] = None,
    authentication_configuration_secret: typing.Optional[_aws_cdk_aws_secretsmanager_ceddda9d.ISecret] = None,
    on_create: typing.Optional[typing.Union[AskSdkCall, typing.Dict[builtins.str, typing.Any]]] = None,
    on_delete: typing.Optional[typing.Union[AskSdkCall, typing.Dict[builtins.str, typing.Any]]] = None,
    on_update: typing.Optional[typing.Union[AskSdkCall, typing.Dict[builtins.str, typing.Any]]] = None,
    removal_policy: typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy] = None,
    timeout: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
) -> None:
    """Type checking stubs"""
    pass
