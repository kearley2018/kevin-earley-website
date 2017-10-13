# Copyright 2015 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Command for creating HTTP2 health checks."""
from googlecloudsdk.api_lib.compute import base_classes
from googlecloudsdk.api_lib.compute import health_checks_utils
from googlecloudsdk.calliope import base
from googlecloudsdk.command_lib.compute.health_checks import flags


@base.ReleaseTracks(base.ReleaseTrack.ALPHA)
class Create(base.CreateCommand):
  """Create a HTTP2 health check to monitor load balanced instances.

  *{command}* is used to create a HTTP2 health check. HTTP2 health checks
  monitor instances in a load balancer controlled by a target pool. All
  arguments to the command are optional except for the name of the health
  check. For more information on load balancing, see
  [](https://cloud.google.com/compute/docs/load-balancing-and-autoscaling/)
  """

  HEALTH_CHECK_ARG = None

  @classmethod
  def Args(cls, parser):
    parser.display_info.AddFormat(flags.DEFAULT_LIST_FORMAT)
    cls.HEALTH_CHECK_ARG = flags.HealthCheckArgument('HTTP2')
    cls.HEALTH_CHECK_ARG.AddArgument(parser, operation_type='create')
    health_checks_utils.AddHttpRelatedCreationArgs(parser)
    health_checks_utils.AddHttpRelatedResponseArg(parser)
    health_checks_utils.AddProtocolAgnosticCreationArgs(parser, 'HTTP2')

  def Run(self, args):
    """Issues the request necessary for adding the health check."""
    holder = base_classes.ComputeApiHolder(self.ReleaseTrack())
    client = holder.client

    health_check_ref = self.HEALTH_CHECK_ARG.ResolveAsResource(
        args, holder.resources)
    proxy_header = client.messages.HTTP2HealthCheck.ProxyHeaderValueValuesEnum(
        args.proxy_header)
    request = client.messages.ComputeHealthChecksInsertRequest(
        healthCheck=client.messages.HealthCheck(
            name=health_check_ref.Name(),
            description=args.description,
            type=client.messages.HealthCheck.TypeValueValuesEnum.HTTP2,
            http2HealthCheck=client.messages.HTTP2HealthCheck(
                host=args.host,
                port=args.port,
                portName=args.port_name,
                requestPath=args.request_path,
                proxyHeader=proxy_header,
                response=args.response),
            checkIntervalSec=args.check_interval,
            timeoutSec=args.timeout,
            healthyThreshold=args.healthy_threshold,
            unhealthyThreshold=args.unhealthy_threshold,
        ),
        project=health_check_ref.project)

    return client.MakeRequests([(client.apitools_client.healthChecks, 'Insert',
                                 request)])
