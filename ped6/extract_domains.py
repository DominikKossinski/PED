from ped5.extract_domains import process_dir as process_domains
from ped5.tokenize_tags import process_dir as process_tags

if __name__ == '__main__':
    process_domains("ped5_trending_original", "ped5_trending_original")
    process_tags("ped5_trending_original", "ped5_trending_original")
