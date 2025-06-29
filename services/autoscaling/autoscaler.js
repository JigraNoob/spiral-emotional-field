const AWS = require('aws-sdk');
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

class AutoScaler {
    constructor() {
        this.scalingPolicies = {
            cpu: {
                upperThreshold: 80,
                lowerThreshold: 20,
                minInstances: 1,
                maxInstances: 10,
                scaleUpCooldown: 300,
                scaleDownCooldown: 300,
                adjustmentType: 'ChangeInCapacity'
            },
            memory: {
                upperThreshold: 80,
                lowerThreshold: 20,
                minInstances: 1,
                maxInstances: 10,
                scaleUpCooldown: 300,
                scaleDownCooldown: 300,
                adjustmentType: 'ChangeInCapacity'
            },
            responseTime: {
                upperThreshold: 1000, // 1 second
                lowerThreshold: 200,
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
            await this.createCloudWatchAlarm(metric, 'scale-up', policy.upperThreshold);
            await this.createCloudWatchAlarm(metric, 'scale-down', policy.lowerThreshold);
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

    // Scale instances
    async scaleInstances(targetCount) {
        await autoscaling.updateAutoScalingGroup({
            AutoScalingGroupName: this.asgName,
            MinSize: targetCount,
            MaxSize: this.scalingPolicies.cpu.maxInstances,
            DesiredCapacity: targetCount
        }).promise();
    }

    // Get scaling metrics
    async getScalingMetrics() {
        const metrics = {};
        
        // Get CPU metrics
        metrics.cpu = await cloudwatch.getMetricStatistics({
            Namespace: 'AWS/EC2',
            MetricName: 'CPUUtilization',
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

        // Get memory metrics
        metrics.memory = await cloudwatch.getMetricStatistics({
            Namespace: 'Spiral/Performance',
            MetricName: 'memory_usage',
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

        // Get response time metrics
        metrics.responseTime = await cloudwatch.getMetricStatistics({
            Namespace: 'Spiral/Performance',
            MetricName: 'response_time',
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

module.exports = AutoScaler;
