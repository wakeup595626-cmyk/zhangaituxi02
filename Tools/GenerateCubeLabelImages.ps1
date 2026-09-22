param(
    [Parameter(Mandatory = $true)]
    [string]$OutputDirectory
)

$ErrorActionPreference = 'Stop'
Add-Type -AssemblyName System.Drawing

if (-not (Test-Path -LiteralPath $OutputDirectory)) {
    [void](New-Item -ItemType Directory -Path $OutputDirectory -Force)
}

$labels = @('时海', '将军', '章鱼哥', '艳丽', '果树', 'old李', '许部长', '冯老板', '谷物')
$width = 1536
$height = 768
$background = [System.Drawing.Color]::FromArgb(255, 29, 17, 22)
$innerBorder = [System.Drawing.Color]::FromArgb(255, 117, 54, 23)
$gold = [System.Drawing.Color]::FromArgb(255, 255, 205, 74)
$shadow = [System.Drawing.Color]::FromArgb(255, 4, 3, 2)

for ($index = 0; $index -lt $labels.Count; $index++) {
    $bitmap = [System.Drawing.Bitmap]::new($width, $height, [System.Drawing.Imaging.PixelFormat]::Format32bppArgb)
    $graphics = [System.Drawing.Graphics]::FromImage($bitmap)
    $graphics.SmoothingMode = [System.Drawing.Drawing2D.SmoothingMode]::AntiAlias
    $graphics.TextRenderingHint = [System.Drawing.Text.TextRenderingHint]::AntiAliasGridFit
    $graphics.Clear($background)

    $outerPen = [System.Drawing.Pen]::new($gold, 22)
    $innerPen = [System.Drawing.Pen]::new($innerBorder, 8)
    $graphics.DrawRectangle($outerPen, 22, 22, $width - 44, $height - 44)
    $graphics.DrawRectangle($innerPen, 56, 56, $width - 112, $height - 112)

    # Use the true glyph bounds rather than a line-layout rectangle.  This makes
    # visual centring reliable for two-, three-, and mixed Latin/Chinese labels.
    $characterCount = $labels[$index].Length
    if ($characterCount -le 2) {
        $fontSize = 320
    } elseif ($characterCount -eq 3) {
        $fontSize = 255
    } else {
        $fontSize = 220
    }
    $font = $null
    do {
        if ($null -ne $font) { $font.Dispose() }
        $font = [System.Drawing.Font]::new('Microsoft YaHei UI', $fontSize, [System.Drawing.FontStyle]::Bold, [System.Drawing.GraphicsUnit]::Pixel)
        $measurePath = [System.Drawing.Drawing2D.GraphicsPath]::new()
        $measurePath.AddString($labels[$index], $font.FontFamily, [int]$font.Style, $font.Size, [System.Drawing.PointF]::new(0, 0), [System.Drawing.StringFormat]::GenericTypographic)
        $measured = $measurePath.GetBounds()
        $measurePath.Dispose()
        $fontSize -= 4
    } while (($measured.Width -gt 820 -or $measured.Height -gt 290) -and $fontSize -gt 24)

    $glyphPath = [System.Drawing.Drawing2D.GraphicsPath]::new()
    $glyphPath.AddString($labels[$index], $font.FontFamily, [int]$font.Style, $font.Size, [System.Drawing.PointF]::new(0, 0), [System.Drawing.StringFormat]::GenericTypographic)
    $glyphBounds = $glyphPath.GetBounds()
    $centerTransform = [System.Drawing.Drawing2D.Matrix]::new()
    $centerTransform.Translate(($width * 0.5) - ($glyphBounds.X + $glyphBounds.Width * 0.5), ($height * 0.5) - ($glyphBounds.Y + $glyphBounds.Height * 0.5))
    $glyphPath.Transform($centerTransform)

    # A symmetric dark outline preserves contrast without shifting the perceived
    # text centre downward as a drop shadow would.
    $outlinePen = [System.Drawing.Pen]::new($shadow, 14)
    $outlinePen.LineJoin = [System.Drawing.Drawing2D.LineJoin]::Round
    $goldBrush = [System.Drawing.SolidBrush]::new($gold)
    $graphics.DrawPath($outlinePen, $glyphPath)
    $graphics.FillPath($goldBrush, $glyphPath)

    $fileName = 'CubeLabelV3_{0:D2}.png' -f ($index + 1)
    $bitmap.Save((Join-Path $OutputDirectory $fileName), [System.Drawing.Imaging.ImageFormat]::Png)

    $goldBrush.Dispose()
    $outlinePen.Dispose()
    $centerTransform.Dispose()
    $glyphPath.Dispose()
    $font.Dispose()
    $innerPen.Dispose()
    $outerPen.Dispose()
    $graphics.Dispose()
    $bitmap.Dispose()
}
