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

class ComplexScaler {
    constructor() {
        this.scalingPolicies = {
            // Time-based scaling
            timeBased: {
                peakHours: {
                    start: '09:00',
                    end: '17:00',
                    minInstances: 3,
                    maxInstances: 15,
                    scaleUpThreshold: 60,
                    scaleDownThreshold: 30
                },
                offHours: {
                    start: '17:00',
                    end: '09:00',
                    minInstances: 1,
                    maxInstances: 5,
                    scaleUpThreshold: 80,
                    scaleDownThreshold: 20
                }
            },

            // Traffic-based scaling
            trafficBased: {
                low: {
                    threshold: 100, // requests/minute
                    minInstances: 1,
                    maxInstances: 3
                },
                medium: {
                    threshold: 500,
                    minInstances: 3,
                    maxInstances: 6
                },
                high: {
                    threshold: 1000,
                    minInstances: 6,
                    maxInstances: 12
                },
                veryHigh: {
                    threshold: 2000,
                    minInstances: 12,
                    maxInstances: 20
                }
            },

            // User behavior-based scaling
            userBehavior: {
                activeUsers: {
                    low: {
                        threshold: 100,
                        minInstances: 1,
                        maxInstances: 3
                    },
                    medium: {
                        threshold: 500,
                        minInstances: 3,
                        maxInstances: 6
                    },
                    high: {
                        threshold: 1000,
                        minInstances: 6,
                        maxInstances: 12
                    }
                },
                sessionDuration: {
                    short: {
                        threshold: 300, // seconds
                        minInstances: 1,
                        maxInstances: 3
                    },
                    medium: {
                        threshold: 900,
                        minInstances: 3,
                        maxInstances: 6
                    },
                    long: {
                        threshold: 1800,
                        minInstances: 6,
                        maxInstances: 12
                    }
                }
            },

            // Resource-based scaling
            resourceBased: {
                cpu: {
                    light: {
                        threshold: 40,
                        minInstances: 1,
                        maxInstances: 3
                    },
                    medium: {
                        threshold: 60,
                        minInstances: 3,
                        maxInstances: 6
                    },
                    heavy: {
                        threshold: 80,
                        minInstances: 6,
                        maxInstances: 12
                    }
                },
                memory: {
                    light: {
                        threshold: 40,
                        minInstances: 1,
                        maxInstances: 3
                    },
                    medium: {
                        threshold: 60,
                        minInstances: 3,
                        maxInstances: 6
                    },
                    heavy: {
                        threshold: 80,
                        minInstances: 6,
                        maxInstances: 12
                    }
                }
            }
        };

        this.asgName = process.env.ASG_NAME;
    }

    // Get current time in hours and minutes
    getCurrentTime() {
        const now = new Date();
        return {
            hours: now.getHours(),
            minutes: now.getMinutes()
        };
    }

    // Determine current time period
    getCurrentTimePeriod() {
        const { hours } = this.getCurrentTime();
        
        if (hours >= 9 && hours < 17) {
            return 'peakHours';
        }
        return 'offHours';
    }

    // Calculate optimal instance count based on multiple metrics
    async calculateOptimalInstanceCount() {
        const metrics = await this.getScalingMetrics();
        
        // Time-based scaling
        const timePeriod = this.getCurrentTimePeriod();
        const timeBasedPolicy = this.scalingPolicies.timeBased[timePeriod];
        
        // Traffic-based scaling
        const trafficLevel = this.determineTrafficLevel(metrics.traffic);
        const trafficPolicy = this.scalingPolicies.trafficBased[trafficLevel];
        
        // User behavior scaling
        const userBehaviorPolicy = this.calculateUserBehaviorPolicy(metrics.userBehavior);
        
        // Resource-based scaling
        const resourcePolicy = this.calculateResourcePolicy(metrics.resources);
        
        // Combine all policies with weights
        const policies = [
            { policy: timeBasedPolicy, weight: 0.3 },
            { policy: trafficPolicy, weight: 0.3 },
            { policy: userBehaviorPolicy, weight: 0.2 },
            { policy: resourcePolicy, weight: 0.2 }
        ];
        
        // Calculate weighted average
        const totalWeight = policies.reduce((sum, p) => sum + p.weight, 0);
        const weightedInstanceCount = policies.reduce((sum, p) => {
            const instances = Math.min(
                p.policy.maxInstances,
                Math.max(p.policy.minInstances, Math.round(p.policy.minInstances + (p.policy.maxInstances - p.policy.minInstances) * (p.weight / totalWeight)))
            );
            return sum + instances;
        }, 0);
        
        return Math.round(weightedInstanceCount);
    }

    // Determine traffic level
    determineTrafficLevel(traffic) {
        if (traffic > this.scalingPolicies.trafficBased.veryHigh.threshold) {
            return 'veryHigh';
        } else if (traffic > this.scalingPolicies.trafficBased.high.threshold) {
            return 'high';
        } else if (traffic > this.scalingPolicies.trafficBased.medium.threshold) {
            return 'medium';
        }
        return 'low';
    }

    // Calculate user behavior policy
    calculateUserBehaviorPolicy(userBehavior) {
        const activeUsers = userBehavior.activeUsers;
        const sessionDuration = userBehavior.sessionDuration;
        
        if (activeUsers > this.scalingPolicies.userBehavior.activeUsers.high.threshold || 
            sessionDuration > this.scalingPolicies.userBehavior.sessionDuration.long.threshold) {
            return this.scalingPolicies.userBehavior.activeUsers.high;
        } else if (activeUsers > this.scalingPolicies.userBehavior.activeUsers.medium.threshold || 
            sessionDuration > this.scalingPolicies.userBehavior.sessionDuration.medium.threshold) {
            return this.scalingPolicies.userBehavior.activeUsers.medium;
        }
        return this.scalingPolicies.userBehavior.activeUsers.low;
    }

    // Calculate resource policy
    calculateResourcePolicy(resources) {
        const cpuUsage = resources.cpu;
        const memoryUsage = resources.memory;
        
        // Use the highest resource usage to determine scaling
        const maxResource = Math.max(cpuUsage, memoryUsage);
        
        if (maxResource > this.scalingPolicies.resourceBased.cpu.heavy.threshold) {
            return this.scalingPolicies.resourceBased.cpu.heavy;
        } else if (maxResource > this.scalingPolicies.resourceBased.cpu.medium.threshold) {
            return this.scalingPolicies.resourceBased.cpu.medium;
        }
        return this.scalingPolicies.resourceBased.cpu.light;
    }

    // Get scaling metrics
    async getScalingMetrics() {
        const metrics = {};
        
        // Get traffic metrics
        metrics.traffic = await cloudwatch.getMetricStatistics({
            Namespace: 'Spiral/Performance',
            MetricName: 'requests_per_minute',
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
        metrics.userBehavior = {
            activeUsers: await cloudwatch.getMetricStatistics({
                Namespace: 'Spiral/Performance',
                MetricName: 'active_users',
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
            }).promise(),
            sessionDuration: await cloudwatch.getMetricStatistics({
                Namespace: 'Spiral/Performance',
                MetricName: 'session_duration',
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
            }).promise()
        };

        // Get resource metrics
        metrics.resources = {
            cpu: await cloudwatch.getMetricStatistics({
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
            }).promise(),
            memory: await cloudwatch.getMetricStatistics({
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
            }).promise()
        };

        return metrics;
    }

    // Scale instances based on metrics
    async scaleBasedOnMetrics() {
        const targetCount = await this.calculateOptimalInstanceCount();
        await autoscaling.updateAutoScalingGroup({
            AutoScalingGroupName: this.asgName,
            MinSize: targetCount,
            MaxSize: targetCount,
            DesiredCapacity: targetCount
        }).promise();
    }
}

module.exports = ComplexScaler;
