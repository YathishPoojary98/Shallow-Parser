open(INFILE,"<@ARGV[0]") or die "Could not open the file $!\n";
@lines = <INFILE>;
open(INTER,">intermediate") or die "Could not create the file $!\n";
foreach $line (@lines)
{
if ($line=~m/(.*)<fs/)
{
print INTER $1,"\n";
#print "PRINTED\n";
}
else
{
print INTER $line;
}
}
close INTER;
close INFILE;
open(FILE1,"<intermediate") or die "Could not open the file $!\n";
open(FILE2,">@ARGV[1]") or die "Could not create the file $!\n";
open(ROOTFILE,"<@ARGV[2]") or die "Could not read the file $!\n";
@roots = ();
@suffs = ();
@gender = ();
@sgpl = ();
@person = ();
@do = ();
@rootlines = <ROOTFILE>;
foreach $line (@rootlines)
{
chomp($line);
@comps = split("\t",$line);
push(@roots,@comps[0]);
push(@suffs,@comps[1]);
push(@gender,@comps[2]);
push(@sgpl,@comps[3]);
push(@person,@comps[4]);
push(@do,@comps[5]);
}
@lines = ();
%fs_dict_single = ('N_NN'=>'n','N_NNP'=>'n','N_NST'=>'nst','PR_PRP'=>'pn','PR_PRF'=>'pn','PR_PRL'=>'pn','PR_PRC'=>'pn','PR_PRQ'=>'pn',
'DM'=>'pn','DM_DMD'=>'pn','DM_DMR'=>'pn','DM_DMQ'=>'pn','V_VM'=>'v','V_VM_VF'=>'v','V_VM_VNF'=>'v','V_VM_VINF'=>'v','V_VM_VNG'=>'v',
'N_NNV'=>'n','V_VAUX'=>'v','V_VM_VNF'=>'v','CC'=>'avy','CC_CCD'=>'avy','CC_CCS'=>'avy','CC_CCS_UT'=>'avy','RP_RPD'=>'avy','RP_CL'=>'n',
'RP_INJ'=>'adj','RP_INTF'=>'adj','QT_QTF'=>'adj','QT_QTC'=>'num','QT_QTO'=>'num','RD_RDF'=>'unk','RD_SYM'=>'punc','RD_PUNC'=>'punc',
'RD_UNK'=>'unk','RD_ECH'=>'n','RD_BUL'=>'unk','PR_PRI'=>'pn','DM_DMI'=>'pn','JJ'=>'adj','RB'=>'adv','PSP'=>'psp','RP_NEG'=>'avy');

%fs_dict_double = ('N__NN'=>'n','N__NNP'=>'n','N__NST'=>'nst','PR__PRP'=>'pn','PR__PRF'=>'pn','PR__PRL'=>'pn','PR__PRC'=>'pn','PR__PRQ'=>'pn',
'DM'=>'pn','DM__DMD'=>'pn','DM__DMR'=>'pn','DM__DMQ'=>'pn','V__VM'=>'v','V__VM__VF'=>'v','V__VM__VNF'=>'v','V__VM__VINF'=>'v','V__VM__VNG'=>'v',
'N__NNV'=>'n','V__VAUX'=>'v','V__VM__VNF'=>'v','CC'=>'avy','CC__CCD'=>'avy','CC__CCS'=>'avy','CC__CCS_UT'=>'avy','RP__RPD'=>'avy','RP__CL'=>'n',
'RP__INJ'=>'adj','RP__INTF'=>'adj','QT__QTF'=>'adj','QT__QTC'=>'num','QT__QTO'=>'num','RD__RDF'=>'unk','RD__SYM'=>'punc','RD__PUNC'=>'punc',
'RD__UNK'=>'unk','RD__ECH'=>'n','RD__BUL'=>'unk','PR__PRI'=>'pn','DM__DMI'=>'pn','JJ'=>'adj','RB'=>'adv','PSP'=>'psp','RP__NEG'=>'avy');
while(<FILE1>)
{
#print "Here\n";
push(@lines,$_);
}
foreach $line (@lines)
{
#print "$line\n";
}
@words = ();
$rcnt=0;
foreach $line (@lines)
{
chomp($line);
if ($line !~ m/\(\(|\)\)|<Sentence/)
{
@word = split('	',$line);
if(@word[1] eq ',')
{
$word_fs = 'COMMA';
}
elsif(@word[1] eq '/-')
{
$word_fs = 'SLASH-HYPHEN';
}
elsif(@word[1] eq '/')
{
$word_fs = 'SLASH';
}
elsif (@word[1]=~m/,/)
{
$word_fs = @word[1] =~ s/,//rg;
}
else
{
$word_fs = @roots[$rcnt];
}
$res = exists($fs_dict_single{@word[2]}) ? $fs_dict_single{@word[2]} : $fs_dict_double{@word[2]};

$d_o = @do[$rcnt];

$per = @person[$rcnt];

if($d_o eq "NULL")
{
$d_o = '';
}

if($per eq "NULL")
{
$per = '';
}

if(@gender[$rcnt] eq 'NULL')
{
$gen='';
}
else
{
$gen = @gender[$rcnt];
}
if(@sgpl[$rcnt] eq 'NULL')
{
$sg_pl='';
}
else
{
$sg_pl = @sgpl[$rcnt];
}
if(((@word[2] eq 'QT_QTC') or (@word[2] eq 'QT__QTC')) and @suffs[$rcnt] eq '0' and $sg_pl eq '')
{
$sg_pl='pl';
}
if(($sg_pl ne 'pl' and $sg_pl ne 'NUM') and ((@word[2] eq 'N_NN') or (@word[2] eq 'N__NN')))
{
$sg_pl='sg';
}
if(@sgpl[$rcnt] eq 'NUM')
{
$sg_pl='';
}
if(($sg_pl ne 'pl') and ((@word[2] eq 'QT_QTO') or (@word[2] eq 'QT__QTO')))
{
$sg_pl='sg';
}
#if (($res eq 'v') and ((@word[2] ne 'V_VM_VNG') and (@word[2] ne 'V__VM__VNG'))) {
    #$d_o = '';
#} else {
    # do nothing, as we don't want to set $d_o to an empty string when $res is not 'v'
#}

if ($res eq 'punc')
{
$fs_string = "<fs af='$word_fs,$res,,,,,,'>";
}
else
{
$fs_string = "<fs af='$word_fs,$res,$gen,$sg_pl,$per,$d_o,@suffs[$rcnt],0'>";
}
if($line =~ m/((.*)	(.*)	([\w_]+))/)
{
if($3 eq '(' || $3 eq ')' || $3 eq '[' || $3 eq ']' || $3 eq '+' || $3 eq '!' || $3 eq '='|| $3 eq '?'  || $3 eq '*')
{
$line = "$2	$3	$4	$fs_string";
}
else
{
$fullstring = "$1	$fs_string";
$line =~ s/$line/$fullstring/;
#print "Line --> $fullstring\n";
}
#print "Word --> $3\n"; 

#print "\$line --> $line\n";

#print "Replaced\n";
}
push(@words,@word[1]);
}
print FILE2 $line,"\n";
if ($line!~m/document/ && $line!~m/\/document/ && $line!~m/head/ && $line!~m/\/head/ && $line!~/Sentence/ && $line!~/\/Sentence/ && $line!~m/\)\)/ && $line!~m/\(\(/)
{
if($line=~m/(.*)	(.*)	(.*)	(.*)/)
{
$rcnt++;
}
}
}
foreach $word (@words)
{
#print "$word\n";
}
@postags = ();
foreach $line (@lines)
{
if ($line =~ m/	(\w+)	/)
{
push(@postags,$1);
}
}

foreach $tag (@postags)
{
#print "$tag\n";
}
#print "Total number of tags : ",scalar @postags,"\n";

close FILE1;
close FILE2;


