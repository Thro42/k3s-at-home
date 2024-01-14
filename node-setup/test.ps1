[void] [System.Reflection.Assembly]::LoadWithPartialName("System.Drawing")
[void] [System.Reflection.Assembly]::LoadWithPartialName("System.Windows.Forms")

# Ini Datei einlesen
$settings = Get-Content nodes\nodes.json | ConvertFrom-JSON

function getOutFile {
    param (
        $filename = ""
    )
    $outfile = $filename
    $DriveName = "D:"
    if ($DriveName -ne "") {
        if (!($DriveName -match '\\$' )) {
            $outpath = -join ($DriveName , '\')
        }
        else {
            $outpath = $DriveName
        }
        $outfile = -join ($outpath , $filename)
    }
    return $outfile
}

function getIPline {
    param (
        $NodeSettings
    )
    $IPAdress = $NodeSettings.ip    
    $ip_line = -join( $IPAdress , '/', $settings.all.ip_mask)
    return $ip_line
}

$ComputerName = "majestix"
$NodeSettings = $settings.${ComputerName}
$outfile = getOutFile("user-data")
Write-Host "file:$($outfile)"

$ipLine = getIPline($NodeSettings)
Write-Host "IP:$($ipLine)"
