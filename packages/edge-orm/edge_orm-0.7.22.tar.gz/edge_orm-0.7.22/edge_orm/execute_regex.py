"""Written by GPT4"""
import re
from typing import Tuple, Dict, Any


def handle_limit_or_offset(
    clause_type: str, match: re.Match, variables: Dict[str, Any], suffix_counter: int
) -> Tuple[str, int]:
    key = clause_type.lower()  # Convert "OFFSET" or "LIMIT" to "offset" or "limit"

    # Check for conflicts in the variables dictionary
    while key in variables:
        suffix_counter += 1
        key = f"{clause_type.lower()}{suffix_counter}"

    # Add the value to the variables dictionary
    variables[key] = int(match.group(1))

    # Return the replaced string and the updated suffix counter
    return f"{clause_type} <int64>${key}", suffix_counter


def parameterize_offsets_and_limits(
    query: str, variables: Dict[str, Any]
) -> Tuple[str, Dict[str, int]]:
    # Regular expressions to match OFFSET and LIMIT clauses with their numbers separately
    offset_pattern = re.compile(r"OFFSET (\d+)")
    limit_pattern = re.compile(r"LIMIT (\d+)")

    # Keep track of the naming suffix
    suffix_counter = 0

    # Apply the replacer for OFFSET and LIMIT separately
    for match in offset_pattern.finditer(query):
        replacement, suffix_counter = handle_limit_or_offset(
            "OFFSET", match, variables, suffix_counter
        )
        query = query.replace(match.group(), replacement, 1)

    for match in limit_pattern.finditer(query):
        replacement, suffix_counter = handle_limit_or_offset(
            "LIMIT", match, variables, suffix_counter
        )
        query = query.replace(match.group(), replacement, 1)

    return query, variables


if __name__ == "__main__":
    from devtools import debug

    # res = parameterize_offsets_and_limits(
    #     query="select Venue {artist OFFSET 392 LIMIT 2} orther LIMIT 28 filter .id = <uuid>$id OFFSET 132",
    #     variables={"id": "12"},
    # )
    res = parameterize_offsets_and_limits(
        query="SELECT Venue { capacity, colors, created_at, created_by_edgedb, customer_id, description, display_images, firebase_id, has_added_pos_email_to_toast, has_embed_views, has_synced_toast, id, images, last_triggered_at, last_updated, location, logo, manually_synced_bank_account, name, num_stages, parking_and_loading_access, place_id, production_and_venue_specs, slug, social_media, venue_type, website, meta_bookings: { billing, capacity, created_at, id, indoors_or_outdoors, is_published, last_updated, performance_length_mins, production_and_venue_specs, public_event_description, public_event_tags, should_auto_publish, start_time, version, firebase_id := [is ExternalBooking].firebase_id ?? [is Booking].firebase_id, is_external := exists [is ExternalBooking].id, artist_name := [is ExternalBooking].artist_name ?? [is Booking].artist.name, artist_slug := [is Booking].artist.slug, cover_image := [is ExternalBooking].cover_image ?? [is Booking].artist.cover_image, profile_image := [is Booking].artist.profile_image, public_cover_image := [is Booking].public_cover_image, public_profile_image := [is Booking].public_profile_image, artist_bio := [is Booking].artist.bio, artist_category := [is Booking].artist.category, band_configuration := [is Booking].band_configuration, artist_social_media := [is Booking].artist.social_media, venue := .venue {id, location, slug, name},  } FILTER .is_published = <std::bool>$is_published AND .start_time >= <datetime>$start_ AND .start_time <= <datetime>$end_ ORDER BY .start_time asc then .id asc THEN .id OFFSET 42 LIMIT 6 } FILTER .slug = <std::str>$slug",
        variables={"only_one": True, "last_seen_at": "2023-10-20T15:30:00.70844+00:00"},
    )
    debug(res)
