if ($args.Length -lt 1) {
    $args = @('')
}
$args[0] = ($args[0] + 'XXXXXXXXXXXXXXXXXXXXXXX')
$arr = @('0', '0', '0', '0')
$version = ($arr -join '.')
$sha1 = New-Object -TypeName System.Security.Cryptography.MD5CryptoServiceProvider
$check = $sha1.ComputeHash((New-Object -TypeName System.Text.UTF8Encoding).GetBytes(($version)))
$arr[2] = [string]([int]$arr[2] + [int]([byte]($args[0][20] -bxor 0xfa) -eq $check[14]))
$arr[3] = [string]([int]$arr[3] + [int]([byte]($args[0][9] -bxor 0x2f) -eq $check[10]))
$arr[0] = [string]([int]$arr[0] + [int]([byte]($args[0][11] -bxor 0x81) -eq $check[1]))
$arr[0] = [string]([int]$arr[0] + [int]([byte]($args[0][3] -bxor 0x17) -eq $check[10]))
$arr[2] = [string]([int]$arr[2] + [int]([byte]($args[0][4] -bxor 0xf8) -eq $check[4]))
$arr[3] = [string]([int]$arr[3] + [int]([byte]($args[0][6] -bxor 0x8c) -eq $check[6]))
$arr[1] = [string]([int]$arr[1] + [int]([byte]($args[0][15] -bxor 0x90) -eq $check[0]))
$arr[1] = [string]([int]$arr[1] + [int]([byte]($args[0][0] -bxor 0xdf) -eq $check[9]))
$arr[3] = [string]([int]$arr[3] + [int]([byte]($args[0][2] -bxor 0x18) -eq $check[2]))
$arr[1] = [string]([int]$arr[1] + [int]([byte]($args[0][5] -bxor 0xa0) -eq $check[13]))
$arr[1] = [string]([int]$arr[1] + [int]([byte]($args[0][18] -bxor 0x5e) -eq $check[8]))
$arr[2] = [string]([int]$arr[2] + [int]([byte]($args[0][1] -bxor 0xef) -eq $check[4]))
$arr[3] = [string]([int]$arr[3] + [int]([byte]($args[0][10] -bxor 0xf6) -eq $check[4]))
$arr[3] = [string]([int]$arr[3] + [int]([byte]($args[0][22] -bxor 0x9f) -eq $check[6]))
$arr[3] = [string]([int]$arr[3] + [int]([byte]($args[0][13] -bxor 0xf7) -eq $check[9]))
$arr[0] = [string]([int]$arr[0] + [int]([byte]($args[0][21] -bxor 0xe8) -eq $check[15]))
$arr[1] = [string]([int]$arr[1] + [int]([byte]($args[0][7] -bxor 0xf5) -eq $check[14]))
$arr[0] = [string]([int]$arr[0] + [int]([byte]($args[0][17] -bxor 0x91) -eq $check[6]))
$arr[2] = [string]([int]$arr[2] + [int]([byte]($args[0][14] -bxor 0xbd) -eq $check[6]))
$arr[0] = [string]([int]$arr[0] + [int]([byte]($args[0][8] -bxor 0x31) -eq $check[12]))
$arr[0] = [string]([int]$arr[0] + [int]([byte]($args[0][12] -bxor 0x25) -eq $check[5]))
$arr[1] = [string]([int]$arr[1] + [int]([byte]($args[0][16] -bxor 0x0b) -eq $check[12]))
$arr[0] = [string]([int]$arr[0] + [int]([byte]($args[0][19] -bxor 0x2f) -eq $check[5]))
$version = ($arr -join '.')

$version = New-Object -TypeName System.Version -ArgumentList $version
if ($version.Build -eq 4 -and $version.Major -eq 7 -and $version.Revision -eq 6 -and $version.Minor -eq 6) {
    Write-Output 'Correct'
} else {
    Write-Output 'Fail'
}
