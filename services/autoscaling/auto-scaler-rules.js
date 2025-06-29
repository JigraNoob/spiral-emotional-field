const AWS = require('aws-sdk');
const { PerformanceObserver, performance } = require('perf_hooks');
const dotenv = require('dotenv');
dotenv.config();

// Configure AWS credentials
AWS.config.update({
    accessKeyId: process.env.AWS_ACCESS_KEY_ID,
    secretAccessKey: process.env.AWS_SECRET_ACCESS_KEY,
    region: process.env.AWS_REGION
});

const autoscaling = new AWS.AutoScaling();
const cloudwatch = new AWS.CloudWatch();

class AutoScalerRules {
    constructor() {
        this.scalingPolicies = {
            diskIo: {
                readThreshold: 10000, // 10000 IOPS
                writeThreshold: 5000, // 5000 IOPS
                minInstances: 1,
                maxInstances: 10,
                scaleUpCooldown: 300,
                scaleDownCooldown: 300,
                adjustmentType: 'ChangeInCapacity'
            },
            apiRateLimit: {
                threshold: 0.8, // 80% of rate limit
                minInstances: 1,
                maxInstances: 15,
                scaleUpCooldown: 300,
                scaleDownCooldown: 300,
                adjustmentType: 'ChangeInCapacity'
            },
            userBehavior: {
                sessionThreshold: 1000,
                actionThreshold: 1000,
                engagementThreshold: 3600, // 1 hour
                minInstances: 1,
                maxInstances: 20,
                scaleUpCooldown: 300,
                scaleDownCooldown: 300,
                adjustmentType: 'ChangeInCapacity'
            },
            thirdPartyService: {
                latencyThreshold: 500, // 500ms
                errorThreshold: 0.01, // 1% error rate
                minInstances: 1,
                maxInstances: 15,
                scaleUpCooldown: 300,
                scaleDownCooldown: 300,
                adjustmentType: 'ChangeInCapacity'
            },
            appHealth: {
                downtimeThreshold: 60, // 60 seconds
                minInstances: 1,
                maxInstances: 10,
                scaleUpCooldown: 300,
                scaleDownCooldown: 300,
                adjustmentType: 'ChangeInCapacity'
            }
        };

        this.asgName = process.env.ASG_NAME;
    }

    // Create scaling policies
    async createScalingPolicies() {
        for (const [metric, policy] of Object.entries(this.scalingPolicies)) {
            // Create scale-up policy
            await autoscaling.putScalingPolicy({
                AutoScalingGroupName: this.asgName,
                PolicyName: `${metric}-scale-up`,
                PolicyType: 'StepScaling',
                AdjustmentType: policy.adjustmentType,
                ScalingAdjustment: 1,
                Cooldown: policy.scaleUpCooldown,
                MetricAggregationType: 'Average'
            }).promise();

            // Create scale-down policy
            await autoscaling.putScalingPolicy({
                AutoScalingGroupName: this.asgName,
                PolicyName: `${metric}-scale-down`,
                PolicyType: 'StepScaling',
                AdjustmentType: policy.adjustmentType,
                ScalingAdjustment: -1,
                Cooldown: policy.scaleDownCooldown,
                MetricAggregationType: 'Average'
            }).promise();

            // Create CloudWatch alarms
            await this.createCloudWatchAlarm(metric, 'scale-up', policy.threshold);
            await this.createCloudWatchAlarm(metric, 'scale-down', policy.threshold);
        }
    }

    // Create CloudWatch alarm
    async createCloudWatchAlarm(metric, direction, threshold) {
        const policyName = `${metric}-${direction}`;
        
        await cloudwatch.putMetricAlarm({
            AlarmName: `${this.asgName}-${policyName}-alarm`,
            ComparisonOperator: direction === 'scale-up' ? 'GreaterThanThreshold' : 'LessThanThreshold',
            EvaluationPeriods: 2,
            MetricName: metric,
            Namespace: 'Spiral/Performance',
            Period: 300,
            Statistic: 'Average',
            Threshold: threshold,
            AlarmActions: [await this.getPolicyArn(policyName)],
            OKActions: [await this.getPolicyArn(policyName)],
            AlarmDescription: `Alarm for ${metric} ${direction} on ${this.asgName}`
        }).promise();
    }

    // Get policy ARN
    async getPolicyArn(policyName) {
        const policies = await autoscaling.describePolicies({
            AutoScalingGroupName: this.asgName,
            PolicyNames: [policyName]
        }).promise();

        return policies.ScalingPolicies[0].PolicyARN;
    }

    // Get current instance count
    async getCurrentInstanceCount() {
        const instances = await autoscaling.describeAutoScalingGroups({
            AutoScalingGroupNames: [this.asgName]
        }).promise();

        return instances.AutoScalingGroups[0].Instances.length;
    }

    // Scale instances based on metrics
    async scaleBasedOnMetrics() {
        const metrics = await this.getMetrics();
        
        // Check disk I/O
        if (metrics.diskIo.read > this.scalingPolicies.diskIo.readThreshold ||
            metrics.diskIo.write > this.scalingPolicies.diskIo.writeThreshold) {
            await this.scaleInstances('diskIo', 'scale-up');
        }

        // Check API rate limits
        if (metrics.apiRateLimit.usage > this.scalingPolicies.apiRateLimit.threshold) {
            await this.scaleInstances('apiRateLimit', 'scale-up');
        }

        // Check user behavior
        if (metrics.userBehavior.sessions > this.scalingPolicies.userBehavior.sessionThreshold ||
            metrics.userBehavior.actions > this.scalingPolicies.userBehavior.actionThreshold ||
            metrics.userBehavior.engagement > this.scalingPolicies.userBehavior.engagementThreshold) {
            await this.scaleInstances('userBehavior', 'scale-up');
        }

        // Check third-party services
        if (metrics.thirdPartyService.latency > this.scalingPolicies.thirdPartyService.latencyThreshold ||
            metrics.thirdPartyService.errorRate > this.scalingPolicies.thirdPartyService.errorThreshold) {
            await this.scaleInstances('thirdPartyService', 'scale-up');
        }

        // Check app health
        if (metrics.appHealth.downtime > this.scalingPolicies.appHealth.downtimeThreshold) {
            await this.scaleInstances('appHealth', 'scale-up');
        }
    }

    // Scale instances
    async scaleInstances(metric, direction) {
        const currentCount = await this.getCurrentInstanceCount();
        const policy = this.scalingPolicies[metric];
        
        let targetCount = currentCount;
        if (direction === 'scale-up') {
            targetCount = Math.min(currentCount + 1, policy.maxInstances);
        } else {
            targetCount = Math.max(currentCount - 1, policy.minInstances);
        }

        await autoscaling.updateAutoScalingGroup({
            AutoScalingGroupName: this.asgName,
            MinSize: targetCount,
            MaxSize: policy.maxInstances,
            DesiredCapacity: targetCount
        }).promise();
    }

    // Get metrics from Prometheus
    async getMetrics() {
        const metrics = {};
        
        // Get disk I/O metrics
        metrics.diskIo = await cloudwatch.getMetricStatistics({
            Namespace: 'Spiral/Performance',
            MetricName: 'disk_io_operations',
            Dimensions: [
                {
                    Name: 'AutoScalingGroupName',
                    Value: this.asgName
                }
            ],
            StartTime: new Date(Date.now() - 300000), // 5 minutes ago
            EndTime: new Date(),
            Period: 300,
            Statistics: ['Average']
        }).promise();

        // Get API rate limit metrics
        metrics.apiRateLimit = await cloudwatch.getMetricStatistics({
            Namespace: 'Spiral/Performance',
            MetricName: 'api_rate_limit_usage',
            Dimensions: [
                {
                    Name: 'AutoScalingGroupName',
                    Value: this.asgName
                }
            ],
            StartTime: new Date(Date.now() - 300000), // 5 minutes ago
            EndTime: new Date(),
            Period: 300,
            Statistics: ['Average']
        }).promise();

        // Get user behavior metrics
        metrics.userBehavior = await cloudwatch.getMetricStatistics({
            Namespace: 'Spiral/Performance',
            MetricName: 'user_behavior',
            Dimensions: [
                {
                    Name: 'AutoScalingGroupName',
                    Value: this.asgName
                }
            ],
            StartTime: new Date(Date.now() - 300000), // 5 minutes ago
            EndTime: new Date(),
            Period: 300,
            Statistics: ['Average']
        }).promise();

        // Get third-party service metrics
        metrics.thirdPartyService = await cloudwatch.getMetricStatistics({
            Namespace: 'Spiral/Performance',
            MetricName: 'third_party_service_health',
            Dimensions: [
                {
                    Name: 'AutoScalingGroupName',
                    Value: this.asgName
                }
            ],
            StartTime: new Date(Date.now() - 300000), // 5 minutes ago
            EndTime: new Date(),
            Period: 300,
            Statistics: ['Average']
        }).promise();

        // Get app health metrics
        metrics.appHealth = await cloudwatch.getMetricStatistics({
            Namespace: 'Spiral/Performance',
            MetricName: 'app_downtime_seconds',
            Dimensions: [
                {
                    Name: 'AutoScalingGroupName',
                    Value: this.asgName
                }
            ],
            StartTime: new Date(Date.now() - 300000), // 5 minutes ago
            EndTime: new Date(),
            Period: 300,
            Statistics: ['Average']
        }).promise();

        return metrics;
    }
}

module.exports = AutoScalerRules;
