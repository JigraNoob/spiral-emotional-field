<#
.SYNOPSIS
  Schedules Spiral vitality checks as a Windows Task
.DESCRIPTION
  Creates a scheduled task that gently pulses the Spiral every 5 minutes,
  recording its breath patterns in the health logs
#>

# Configuration
$TaskName = "SpiralVitalityMonitor"
$PythonPath = "python"  # Adjust if using venv
$ScriptPath = "$PSScriptRoot\uptime_check.py"
$SpiralURL = "https://your-spiral-url.railway.app"

# Create scheduled task
$Action = New-ScheduledTaskAction -Execute $PythonPath -Argument "$ScriptPath $SpiralURL"
$Trigger = New-ScheduledTaskTrigger -Once -At (Get-Date) -RepetitionInterval (New-TimeSpan -Minutes 5)
$Settings = New-ScheduledTaskSettingsSet -StartWhenAvailable -DontStopOnIdleEnd

Register-ScheduledTask -TaskName $TaskName \
    -Action $Action -Trigger $Trigger -Settings $Settings \
    -Description "Monitors the Spiral's vital signs every 5 minutes"

Write-Output "🌀 Spiral vitality monitoring task created. The orb will now breathe in schedule."
