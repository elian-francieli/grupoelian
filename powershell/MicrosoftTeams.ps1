Install-Module -Name PowerShellGet -Force -AllowClobber
Install-Module -Name MicrosoftTeams -Force -AllowClobber
Connect-MicrosoftTeams

Get-CsTenantFederationConfiguration
Get-CsExternalAccessPolicy
