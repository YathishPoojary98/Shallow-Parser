open(INFILE,"<@ARGV[0]") or die "Could not read the file $!\n";
@lines = <INFILE>;
close INFILE;
open(OUTFILE,">@ARGV[0]") or die "Could not open the file $!\n";
foreach $line (@lines)
{
chomp($line);
if ($line=~m/(.*)	(.*)	(.*)$/ || $line=~m/(.*)	(.*)	(.*)	<fs/)
{
$line=~s/_/__/g;
}
print OUTFILE $line,"\n";
}
close OUTFILE;
