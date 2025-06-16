import os
import json
from datetime import datetime, time, date # Added date for get_daily_context
import swisseph as swe  # Astrology engine only
from typing import Union # Import Union for type hinting

from datetime import datetime, date # For handling dates


# -from datetime import datetime, date
from datetime import datetime

class UserProfile:
    def __init__(self, name, dob_str, birthtime_str=None, birthplace=None):
        self.name = name
        self.birthdate = datetime.strptime(dob_str, "%Y-%m-%d").date()

        if birthtime_str:
            self.birthtime = datetime.strptime(birthtime_str, "%H:%M").time()
        else:
            self.birthtime = None

        self.birthplace = birthplace

        # Initialize missing attributes
        self.numerology_profile = {}
        self.astrology_profile = {}
        self.feedback = {}
        self.feedback_log = []  # ← this was missing


    
    def update_numerology(self, numerology_data, target_date=None):
        if target_date:
            if not isinstance(target_date, str):
                try:
                    target_date = target_date.strftime("%Y-%m-%d")
                except AttributeError:
                    raise ValueError("target_date must be a YYYY-MM-DD string or a date/datetime object.")
            self.numerology_profile[target_date] = numerology_data
        else:
            self.numerology_profile = numerology_data

    def update_astrology(self, astrology_data, target_date=None):
        if target_date:
            if not isinstance(target_date, str):
                try:
                    target_date = target_date.strftime("%Y-%m-%d")
                except AttributeError:
                    raise ValueError("target_date must be a YYYY-MM-DD string or a date/datetime object.")
            self.astrology_profile[target_date] = astrology_data
        else:
            self.astrology_profile = astrology_data

    def log_feedback(self, feedback_date, rating, notes):
        if isinstance(feedback_date, (datetime, date)):
            date_str = feedback_date.strftime("%Y-%m-%d")
        elif isinstance(feedback_date, str):
            try:
                datetime.strptime(feedback_date, "%Y-%m-%d")
                date_str = feedback_date
            except ValueError:
                raise ValueError("feedback_date string must be in YYYY-MM-DD format.")
        else:
            raise TypeError("feedback_date must be a datetime/date or YYYY-MM-DD string.")


        self.feedback_log.append({
            "date": date_str,
            "rating": rating,
            "notes": notes,
            "astro_context_snapshot": self.astrology_profile.get(date_str, {}), # Store snapshot at time of feedback
            "num_context_snapshot": self.numerology_profile.get(date_str, {})  # Store snapshot at time of feedback
        })

    def to_dict(self):
        """Converts the UserProfile object to a dictionary for JSON serialization."""
        return {
            "name": self.name,
            "birthdate": self.birthdate.strftime("%Y-%m-%d"),
            "birthtime": self.birthtime.strftime("%H:%M") if self.birthtime else None,
            "birthplace": self.birthplace,
            "numerology_profile": self.numerology_profile, # Assumes this is already JSON serializable
            "astrology_profile": self.astrology_profile,   # Assumes this is already JSON serializable
            "feedback_log": self.feedback_log             # Assumes this is already JSON serializable
        }

    def save_to_file(self, file_path: str):
        """Saves the UserProfile data to a JSON file."""
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(self.to_dict(), f, indent=4, ensure_ascii=False)
            print(f"UserProfile for {self.name} saved to {file_path}")
        except IOError as e:
            print(f"Error saving UserProfile to {file_path}: {e}")
        except TypeError as e:
            print(f"Error serializing UserProfile data for {self.name}: {e}")

    @classmethod
    def load_from_file(cls, file_path: str):
        """Loads a UserProfile instance from a JSON file."""
        if not os.path.exists(file_path):
            print(f"Error: File not found at {file_path}")
            return None
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # Get the string representations from the loaded data
            dob_str_from_file = data["birthdate"] # Expected to be "YYYY-MM-DD"
            birthtime_str_from_file = data.get("birthtime") # Expected to be "HH:MM" or None

            # Create the UserProfile instance using the constructor's expected arguments
            profile_instance = cls(
                name=data["name"],
                dob_str=dob_str_from_file,
                birthtime_str=birthtime_str_from_file,
                birthplace=data.get("birthplace")
            )

            # Set the additional attributes on the created instance
            profile_instance.numerology_profile = data.get("numerology_profile", {})
            profile_instance.astrology_profile = data.get("astrology_profile", {})
            profile_instance.feedback_log = data.get("feedback_log", [])

            return profile_instance
        except IOError as e:
            print(f"Error loading UserProfile from {file_path}: {e}")
            return None
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON from {file_path}: {e}")
            return None
        except KeyError as e:
            print(f"Missing essential key in JSON data from {file_path}: {e}")
            return None
        except Exception as e:
            print(f"An unexpected error occurred loading UserProfile from {file_path}: {e}")
            return None

    def get_daily_context(self, target_date: Union[str, datetime, date]):
        """
        Retrieves the astrological and numerological context for a specific date.
        target_date can be a YYYY-MM-DD string, or a datetime/date object.
        """
        if isinstance(target_date, (datetime, date)):
            date_str = target_date.strftime("%Y-%m-%d")
        elif isinstance(target_date, str):
            try:
                # Validate date string format
                datetime.strptime(target_date, "%Y-%m-%d")
                date_str = target_date
            except ValueError:
                raise ValueError("target_date string must be in YYYY-MM-DD format.")
        else:
            raise TypeError("target_date must be a datetime/date object or a YYYY-MM-DD string.")

        return {
            "date": date_str,
            "numerology": self.numerology_profile.get(date_str, {}),
            "astrology": self.astrology_profile.get(date_str, {})
        }


    def __repr__(self):
        return (
            f"UserProfile(name='{self.name}', birthdate='{self.birthdate.strftime('%Y-%m-%d')}', "
            f"birthtime='{self.birthtime.strftime('%H:%M') if self.birthtime else None}', birthplace='{self.birthplace}')"
        )

if __name__ == '__main__':
    # --- Test UserProfile Creation ---
    print("--- Testing UserProfile Creation ---")
    try:
        user1 = UserProfile(
            name="jeffrey allen louis weber",
            dob_str="1987-05-08",
            birthtime_str="02:45", # Ensure HH:MM format if providing
            birthplace="redding , California"
        )
        print(user1)

        user_no_time = UserProfile(
            name="Bob The Builder",
            dob_str="1985-12-01",
            birthplace="Constructville"
        )
        print(user_no_time)

        # Test with datetime object for birthdate and time object for birthtime
        bday_dt_str = datetime(1992, 5, 10).strftime("%Y-%m-%d")
        btime_t_str = time(8, 15).strftime("%H:%M")
        user_dt_obj = UserProfile(
            name="Carol Danvers",
            dob_str=bday_dt_str,
            birthtime_str=btime_t_str,
            birthplace="Boston, MA"
        )
        print(user_dt_obj)


    except ValueError as e:
        print(f"Error creating profile: {e}")

    # --- Test Updating Profiles ---
    print("\n--- Testing Profile Updates ---")
    if 'user1' in locals():
        sample_numerology_day1 = {"personal_day": "1", "personal_month": "8", "personal_year": "1"}
        sample_astrology_day1 = {"moon_sign": "Aries", "mercury_retrograde": False}
        user1.update_numerology(sample_numerology_day1, "2024-05-29")
        user1.update_astrology(sample_astrology_day1, "2024-05-29")
        print(f"Alice's Numerology for 2024-05-29: {user1.numerology_profile.get('2024-05-29')}")
        print(f"Alice's Astrology for 2024-05-29: {user1.astrology_profile.get('2024-05-29')}")

        # Update entire profile (less common for daily, but for completeness)
        user_no_time.update_numerology({"overall_lifepath": "5"})
        print(f"Bob's Numerology (overall): {user_no_time.numerology_profile}")


    # --- Test Logging Feedback ---
    print("\n--- Testing Feedback Logging ---")
    if 'user1' in locals():
        user1.log_feedback("2024-05-29", "Positive", "Great start to the project!")
        user1.log_feedback(datetime(2024,5,30), "Neutral", "Routine day, nothing special.")
        print(f"Alice's Feedback Log: {json.dumps(user1.feedback_log, indent=2)}")

    # --- Test get_daily_context ---
    print("\n--- Testing get_daily_context ---")
    if 'user1' in locals():
        context_day1 = user1.get_daily_context("2024-05-29")
        print(f"Context for Alice on 2024-05-29: {json.dumps(context_day1, indent=2)}")
        context_day_nodata = user1.get_daily_context("2024-01-01") # Date with no specific data
        print(f"Context for Alice on 2024-01-01: {json.dumps(context_day_nodata, indent=2)}")

    # --- Test Save and Load ---
    print("\n--- Testing Save and Load ---")
    profile_file_path = "test_user_profile.json"
    if 'user1' in locals():
        user1.save_to_file(profile_file_path)
        loaded_user1 = UserProfile.load_from_file(profile_file_path)

        if loaded_user1:
            print(f"Loaded User: {loaded_user1}")
            print(f"Original Name: {user1.name}, Loaded Name: {loaded_user1.name}")
            print(f"Original Birthdate: {user1.birthdate.date()}, Loaded Birthdate: {loaded_user1.birthdate.date()}")
            print(f"Original Birthtime: {user1.birthtime}, Loaded Birthtime: {loaded_user1.birthtime}")
            print(f"Original Numerology (2024-05-29): {user1.numerology_profile.get('2024-05-29')}")
            print(f"Loaded Numerology (2024-05-29): {loaded_user1.numerology_profile.get('2024-05-29')}")
            print(f"Loaded Feedback Log Length: {len(loaded_user1.feedback_log)}")
            if loaded_user1.feedback_log:
                print(f"First loaded feedback entry date: {loaded_user1.feedback_log[0]['date']}")

        # Clean up test file
        if os.path.exists(profile_file_path):
            os.remove(profile_file_path)
            print(f"Cleaned up {profile_file_path}")
    else:
        print("Skipping save/load test as user1 was not created.")

    print("\n--- Test UserProfile with no optional data on load ---")
    # Create a minimal JSON to simulate loading a profile that was saved with minimal data
    minimal_data = {
        "name": "Minimal User",
        "birthdate": "2000-01-01",
        "birthtime": None,
        "birthplace": "Somewhere"
        # numerology_profile, astrology_profile, feedback_log are omitted
    }
    minimal_file_path = "minimal_profile.json"
    with open(minimal_file_path, 'w') as f:
        json.dump(minimal_data, f, indent=4)

    loaded_minimal_user = UserProfile.load_from_file(minimal_file_path)
    if loaded_minimal_user:
        print(f"Loaded Minimal User: {loaded_minimal_user}")
        print(f"  Numerology Profile: {loaded_minimal_user.numerology_profile}") # Should be {}
        print(f"  Astrology Profile: {loaded_minimal_user.astrology_profile}")   # Should be {}
        print(f"  Feedback Log: {loaded_minimal_user.feedback_log}")           # Should be []
    if os.path.exists(minimal_file_path):
        os.remove(minimal_file_path)
        print(f"Cleaned up {minimal_file_path}")