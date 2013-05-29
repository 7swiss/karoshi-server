package ParseBash;

use strict;

sub _trim(\$);

sub new {
	my ($className, @files) = @_;
	my $self = {};
	$self->{filename} = undef;
	$self->{variables} = {};
	
	bless($self, $className);
	foreach my $bashFile (@files) {
		$self->parseFile($bashFile);
	}
	return $self;
}

sub parseFile {
	my ($self, $bashFile) = @_;
	
	open my $fileHandle, $bashFile or return 0;
	$self->{filename} = $bashFile;
	
	while (my $line = <$fileHandle>) {
		chomp $line;
		_trim $line;
		next if (substr($line, 0, 1) eq '#');
		my ($var, $data) = split /=/, $line, 2;
		$data =~ s/^(['"])(.*)\1/$2/;
		$self->{variables}->{$var} = $data;
	}
	
	close $fileHandle;
	return 1;
}

sub var {
	my ($self, $varName, $value) = @_;
	if ($value) {
		return $self->{variables}->{$varName} = $value;
	} else {
		return $self->{variables}->{$varName};
	}
}

####################
#Private subroutines
####################

sub _trim(\$)
{
	my $stringRef = shift;
	$$stringRef =~ s/^\s+//;
	$$stringRef =~ s/\s+$//;
}

1;