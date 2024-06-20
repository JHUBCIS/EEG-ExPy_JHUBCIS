# !Make sure to add a rule in Windows Defender Firewall with Advanced Security to allow UDP traffic on port 1000 (or another port of your preference).
# In case of doubt enter the following command in powershell:
#> netsh advfirewall firewall add rule name="Open UDP Port 1000" dir=in action=allow protocol=UDP localport=1000

# Create a new UDP client
$udpClient = New-Object System.Net.Sockets.UdpClient(1000)
$endpoint = New-Object System.Net.IPEndPoint([System.Net.IPAddress]::Any, 0)

Write-Host "Listening for UDP packets on port 1000..."

while ($true) {
    # Receive data from the UDP client
    $receivedBytes = $udpClient.Receive([ref]$endpoint)
    $receivedData = [System.Text.Encoding]::ASCII.GetString($receivedBytes)
    Write-Host "Received data: $receivedData from $($endpoint.Address):$($endpoint.Port)"
}

# !Make sure to kill the running PowerShell terminal before collecting data with Unicorn Recorder!