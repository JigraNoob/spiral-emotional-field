const nodemailer = require('nodemailer');
const slack = require('@slack/webhook');
const twilio = require('twilio');
const dotenv = require('dotenv');
dotenv.config();

class AlertManager {
    constructor() {
        // Initialize notification services
        this.emailTransport = nodemailer.createTransport({
            service: 'gmail',
            auth: {
                user: process.env.EMAIL_USER,
                pass: process.env.EMAIL_PASS
            }
        });

        this.slackWebhook = new slack(process.env.SLACK_WEBHOOK_URL);

        this.twilioClient = twilio(
            process.env.TWILIO_ACCOUNT_SID,
            process.env.TWILIO_AUTH_TOKEN
        );

        // Alert thresholds
        this.thresholds = {
            performance: {
                warning: 0.8,
                critical: 0.95
            },
            error: {
                warning: 0.05,
                critical: 0.1
            },
            memory: {
                warning: 0.8,
                critical: 0.9
            }
        };
    }

    // Alert types
    async sendEmail(recipients, subject, message) {
        const mailOptions = {
            from: process.env.EMAIL_USER,
            to: recipients,
            subject,
            text: message
        };

        try {
            await this.emailTransport.sendMail(mailOptions);
            return true;
        } catch (error) {
            console.error('Failed to send email:', error);
            return false;
        }
    }

    async sendSlack(message) {
        try {
            await this.slackWebhook.send(message);
            return true;
        } catch (error) {
            console.error('Failed to send Slack message:', error);
            return false;
        }
    }

    async sendSMS(phoneNumber, message) {
        try {
            await this.twilioClient.messages.create({
                body: message,
                from: process.env.TWILIO_PHONE_NUMBER,
                to: phoneNumber
            });
            return true;
        } catch (error) {
            console.error('Failed to send SMS:', error);
            return false;
        }
    }

    // Alert levels
    async sendAlert(alertType, level, message, data = {}) {
        const recipients = this.getRecipients(level);
        
        // Send notifications based on alert level
        if (level === 'critical') {
            // Critical alerts: email, Slack, and SMS
            await Promise.all([
                this.sendEmail(recipients.email, `CRITICAL: ${alertType}`, message),
                this.sendSlack(`*CRITICAL*: ${message}`),
                this.sendSMS(recipients.phone, `CRITICAL: ${message}`)
            ]);
        } else if (level === 'warning') {
            // Warning alerts: email and Slack
            await Promise.all([
                this.sendEmail(recipients.email, `WARNING: ${alertType}`, message),
                this.sendSlack(`*WARNING*: ${message}`)
            ]);
        } else {
            // Info alerts: Slack only
            await this.sendSlack(`*INFO*: ${message}`);
        }

        // Log the alert
        console.log(`Alert sent - Type: ${alertType}, Level: ${level}, Message: ${message}`);
    }

    // Get recipients based on alert level
    getRecipients(level) {
        const baseRecipients = {
            email: process.env.ALERT_EMAIL.split(','),
            phone: process.env.ALERT_PHONE.split(',')
        };

        if (level === 'critical') {
            return {
                email: [...baseRecipients.email, ...process.env.CRITICAL_EMAIL.split(',')],
                phone: [...baseRecipients.phone, ...process.env.CRITICAL_PHONE.split(',')]
            };
        }

        return baseRecipients;
    }

    // Performance alerts
    async checkPerformanceMetrics(metrics) {
        const { network, api, memory, dom, audio, websocket } = metrics;
        
        // Check network performance
        if (network) {
            Object.entries(network).forEach(([url, data]) => {
                if (data.duration > this.thresholds.performance.critical * data.maxResponseTime) {
                    this.sendAlert('network', 'critical', `
                        Network request to ${url} is critically slow:
                        Duration: ${data.duration}ms
                        Status: ${data.status}
                        Size: ${data.size} bytes
                    `);
                } else if (data.duration > this.thresholds.performance.warning * data.maxResponseTime) {
                    this.sendAlert('network', 'warning', `
                        Network request to ${url} is slow:
                        Duration: ${data.duration}ms
                        Status: ${data.status}
                        Size: ${data.size} bytes
                    `);
                }
            });
        }

        // Check API performance
        if (api) {
            Object.entries(api).forEach(([endpoint, data]) => {
                if (data.duration > this.thresholds.performance.critical * data.maxResponseTime) {
                    this.sendAlert('api', 'critical', `
                        API endpoint ${endpoint} is critically slow:
                        Duration: ${data.duration}ms
                        Status: ${data.status}
                        Success: ${data.success}
                    `);
                } else if (data.duration > this.thresholds.performance.warning * data.maxResponseTime) {
                    this.sendAlert('api', 'warning', `
                        API endpoint ${endpoint} is slow:
                        Duration: ${data.duration}ms
                        Status: ${data.status}
                        Success: ${data.success}
                    `);
                }
            });
        }

        // Check memory usage
        if (memory) {
            if (memory.heapUsed > this.thresholds.memory.critical * memory.heapTotal) {
                this.sendAlert('memory', 'critical', `
                    Memory usage is critically high:
                    Heap Used: ${memory.heapUsed} bytes
                    Heap Total: ${memory.heapTotal} bytes
                    External: ${memory.external} bytes
                `);
            } else if (memory.heapUsed > this.thresholds.memory.warning * memory.heapTotal) {
                this.sendAlert('memory', 'warning', `
                    Memory usage is high:
                    Heap Used: ${memory.heapUsed} bytes
                    Heap Total: ${memory.heapTotal} bytes
                    External: ${memory.external} bytes
                `);
            }
        }

        // Check DOM complexity
        if (dom) {
            Object.entries(dom).forEach(([key, value]) => {
                if (value > this.thresholds.dom[key]) {
                    this.sendAlert('dom', 'warning', `
                        DOM complexity is high:
                        ${key}: ${value}
                        Threshold: ${this.thresholds.dom[key]}
                    `);
                }
            });
        }

        // Check audio performance
        if (audio) {
            if (audio.latency > this.thresholds.audio.maxLatency) {
                this.sendAlert('audio', 'warning', `
                    Audio latency is high:
                    Latency: ${audio.latency}ms
                    Sample Rate: ${audio.sampleRate}Hz
                `);
            }
        }

        // Check WebSocket performance
        if (websocket) {
            if (websocket.connection.duration > this.thresholds.websocket.maxConnectionTime) {
                this.sendAlert('websocket', 'warning', `
                    WebSocket connection time is high:
                    Duration: ${websocket.connection.duration}ms
                    Success: ${websocket.connection.success}
                `);
            }
        }
    }

    // Error alerts
    async handleError(error, context = {}) {
        const level = error.severity || 'error';
        
        const message = `
            Error: ${error.message}
            Stack: ${error.stack}
            Context: ${JSON.stringify(context)}
        `;

        await this.sendAlert('error', level, message);
    }
}

module.exports = AlertManager;
