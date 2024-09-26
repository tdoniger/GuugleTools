import sys
import re
pairs_snos = []
# snos_loc = []
pairs_mRNAs = []
# mRNA_loc = []
pairs_match = []
mRNA_locs = []  ###
snos_locs = []  ###
mRNA_match_seq=[]
snoRNA_match_seq=[]
#columns = ['snoRNA', 'snoRNA_loc', 'mRNA', 'mRNA_loc', 'basepairing','mRNA_seq','snoRNA_seq']

def guugle_to_bed(input_file, output_file):
    with open(input_file, 'r') as results, open(output_file, 'w') as outfile:
        sno = None
        mRNA = None
        mRNA_match = None
        sno_match = None
        snoRNA_loc = None
        mRNA_loc = None
        hit_len= None
        for line in results:
            if line.startswith("Match"):
                l = line.strip().split('\"')
                h_l = l[0].split(':')
                hit_len=h_l[1].strip()
                #print(hit_len)
                s = l[3].strip('\"').split()
                sno = s[0]
                snoRNA_loc = l[4]
                snoRNA_loc = snoRNA_loc.strip(" at vs.")
                # print(snoRNA_loc)
                m = l[1].strip('\"').split('|')
                mRNA = m[0]
                mRNA_loc = l[2]
                mRNA_loc = mRNA_loc.strip(" at vs.")
                # print(mRNA_loc)
                pairs_snos.append(sno)
                pairs_mRNAs.append(mRNA)
                mRNA_locs.append(mRNA_loc)
                snos_locs.append(snoRNA_loc)
                chrom = sno
                start = int(snoRNA_loc) - 1  # BED format is 0-based
                end = int(snoRNA_loc)+int(hit_len)-1
                name = mRNA
                score = int(0)  # Convert score to integer
                strand = "+"
            
                # Write in BED format
                bed_line = f"{chrom}\t{start}\t{end}\t{name}\t{score}\t{strand}\n"
                outfile.write(bed_line)

            elif line.startswith("5"):
                mRNA_match = line.strip()
            elif line.startswith("3"):
                sno_match = line.strip()
            elif None not in (sno, mRNA, sno_match, mRNA_match):
                sno = None
                mRNA = None
                sno_match = None
                mRNA_match = None
                snoRNA_loc = None
                mRNA_loc = None

                
            else:
                continue

            

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python guugle_to_bed.py input_file output_file")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    guugle_to_bed(input_file, output_file)
    print(f"Conversion complete. BED file written to {output_file}")
