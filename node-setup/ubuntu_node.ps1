[void] [System.Reflection.Assembly]::LoadWithPartialName("System.Drawing")
[void] [System.Reflection.Assembly]::LoadWithPartialName("System.Windows.Forms")

# Ini Datei einlesen
$settings = Get-Content nodes\nodes.json | ConvertFrom-JSON

function getOutFile {
    param (
        $filename = ""
    )
    $outfile = $filename
    $DriveName = $objCombobox2.SelectedItem.Trim()
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
    Write-Host "IP:$($IPAdress)"
    $ip_line = -join ($IPAdress , '/', $settings.all.ip_mask)
    return $ip_line
}
function ubuntuSD ( $NodeSettings,  ) {
    $ip_line = ""
    $outfile = getOutFile( $NodeSettings )
    $nameservers = [String]::Join(',',$settings.all.nameservers)
    switch ($NodeSettings.network) {
        'eth' {  
            $FirstStart = Get-Content templates\ubuntu\user-data
            $FirstStart.replace('[hostname]', $ComputerName).`
                        replace('[passwd]', $settings.all.passwd).`
                        replace('[passwd]', $settings.all.passwd).`
                        replace('[ssh-rsa]', $settings.all.ssh_rsa).`
                        replace('[username]',$settings.all.firstuser)`
                        -join "`n" | Set-Content -NoNewline $outfile
        }
        'wifi' {  }
        Default {}
    }
    $ipfile = -join ($outpath , 'network-config')
    Write-Host 'Prepare' $ipfile 'for' $IPAdress 'on' $NodeSettings.networ
    switch ($NodeSettings.network) {
        'eth' {  
            $interface = Get-Content templates\ubuntu\network-config.eth
            $interface.replace('[ip_address]', $ip_line).`
                       replace('[gateway]',$settings.all.gateway).`
                       replace('[nameservers]',$nameservers).`
                       replace('[local-domain]',$settings.all.domain)`
                       -join "`n" | Set-Content -NoNewline $ipfile

        }
        Default {}
    }
} 


function SetupSD { 
    Write-Host "selekted Node:$($objCombobox.SelectedItem)"
    if ($objCombobox.SelectedItem) {
        $ComputerName = $objCombobox.SelectedItem.Trim()
        if ($ComputerName -ne "") {
            $NodeSettings = $settings.${ComputerName}
            $IPAdress = $NodeSettings.ip    
            Write-Host "IP:$($IPAdress)"
            $ip_line = -join ($IPAdress , '/16')
            if ($objCombobox2.SelectedItem) {
                $DriveName = $objCombobox2.SelectedItem.Trim()
                if ($DriveName -ne "") {
                    Write-Host "Drive:$($DriveName)"
                    if (!($DriveName -match '\\$' )) {
                        $outpath = -join ($DriveName , '\')
                    }
                    else {
                        $outpath = $DriveName
                    }
                    Write-Host "Output:$($outpath)"
                    $outfile = -join ($outpath , 'user-data')
                    Write-Host 'Prepare' $outfile 'for' $ComputerName
                    switch ($NodeSettings.os) {
                        'ubuntu' {

                            $nameservers = [String]::Join(',',$settings.all.nameservers)
                            switch ($NodeSettings.network) {
                                'eth' {  
                                    $FirstStart = Get-Content templates\ubuntu\user-data
                                    $FirstStart.replace('[hostname]', $ComputerName).`
                                                replace('[passwd]', $settings.all.passwd).`
                                                replace('[passwd]', $settings.all.passwd).`
                                                replace('[ssh-rsa]', $settings.all.ssh_rsa).`
                                                replace('[username]',$settings.all.firstuser)`
                                                -join "`n" | Set-Content -NoNewline $outfile
                                }
                                'wifi' {  }
                                Default {}
                            }
                            $ipfile = -join ($outpath , 'network-config')
                            Write-Host 'Prepare' $ipfile 'for' $IPAdress 'on' $NodeSettings.networ
                            switch ($NodeSettings.network) {
                                'eth' {  
                                    $interface = Get-Content templates\ubuntu\network-config.eth
                                    $interface.replace('[ip_address]', $ip_line).`
                                               replace('[gateway]',$settings.all.gateway).`
                                               replace('[nameservers]',$nameservers).`
                                               replace('[local-domain]',$settings.all.domain)`
                                               -join "`n" | Set-Content -NoNewline $ipfile

                                }
                                Default {}
                            }
                        }
                        Default {
                            $nameservers = [String]::Join(' ',$settings.all.nameservers)

                        }
                    }
                }
            }
        }
    }
#    $objForm.Close()
}

$objForm = New-Object System.Windows.Forms.Form
$objForm.Size = New-Object System.Drawing.Size(500,300)
$objForm.Text = "Waehle den Node aus"

$objLabel = New-Object System.Windows.Forms.Label
$objLabel.Location = New-Object System.Drawing.Size(20,40)
$objLabel.Size = New-Object System.Drawing.Size(60,20)
$objLabel.Text = "Node:"
$objForm.Controls.Add($objLabel)

$objCombobox = New-Object System.Windows.Forms.Combobox 
$objCombobox.Location = New-Object System.Drawing.Size(80,40) 
$objCombobox.Size = New-Object System.Drawing.Size(200,20) 
$objCombobox.Height = 70
$objForm.Controls.Add($objCombobox) 
$objForm.Topmost = $True
$objForm.Add_Shown({$objForm.Activate()})
#$objCombobox.Items.AddRange($computer) #Computer werden aus der Variable geladen und angezeigt
#Write-Host 'settings' $settings
$settings_str = "$($settings)"
$nodes = $settings_str.Split("=;")
foreach ($node in $nodes) {
    if ($node -ne "" -and $node -ne "@{all" -and $node -ne "}" ) {
       $idx = $objCombobox.Items.Add($node)
#        Write-Host 'Prepare' $node
    }
}
#   $objCombobox.SelectedItem #ausgewählter Computername wird übernommen

$objLabel2 = New-Object System.Windows.Forms.Label
$objLabel2.Location = New-Object System.Drawing.Size(20,60)
$objLabel2.Size = New-Object System.Drawing.Size(60,20)
$objLabel2.Text = "Drive:"
$objForm.Controls.Add($objLabel2)

$objCombobox2 = New-Object System.Windows.Forms.Combobox 
$objCombobox2.Location = New-Object System.Drawing.Size(80,60) 
$objCombobox2.Size = New-Object System.Drawing.Size(200,20) 
$objCombobox2.Height = 70
$objForm.Controls.Add($objCombobox2) 
#$objForm.Topmost = $True
#$objForm.Add_Shown({$objForm.Activate()})

$drives =  (Get-WmiObject Win32_LogicalDisk).DeviceID
foreach ($drive in $drives) {
    $idx = $objCombobox2.Items.Add($drive)
}

#$driveSelect = New-Object System.Windows.Forms.
   #OK Button anzeigen lassen
   $OKButton = New-Object System.Windows.Forms.Button
   $OKButton.Location = New-Object System.Drawing.Size(300,220)
   $OKButton.Size = New-Object System.Drawing.Size(75,23)
   $OKButton.Text = "OK"
   $OKButton.Name = "OK"
   #$OKButton.DialogResult = "OK" # Ansonsten wird Fenster geschlossen
   $OKButton.Add_Click({ SetupSD })
   $objForm.Controls.Add($OKButton) 


   #Abbrechen Button
   $CancelButton = New-Object System.Windows.Forms.Button
   $CancelButton.Location = New-Object System.Drawing.Size(400,220)
   $CancelButton.Size = New-Object System.Drawing.Size(75,23)
   $CancelButton.Text = "Abbrechen"
   $CancelButton.Name = "Abbrechen"
   $CancelButton.DialogResult = "Cancel"
   $CancelButton.Add_Click({$objForm.Close()})
   $objForm.Controls.Add($CancelButton) 


######################################################################################################

        
# Die letzte Zeile sorgt dafür, dass unser Fensterobjekt auf dem Bildschirm angezeigt wird.
[void] $objForm.ShowDialog()