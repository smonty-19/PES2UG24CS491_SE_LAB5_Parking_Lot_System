"""Simple parking lot management system.

Handles parking/releasing vehicles, fee calculation, ticket generation
and exporting a manifest of the current slot state.
"""
# FIX (C0114): added module docstring.

import hashlib
import os
import secrets  # FIX (B311): use 'secrets' instead of 'random' for PINs.

# FIX (F401/W0611): removed unused 'import math'.
# FIX (B605): 'os' is now only used to read the secret from the environment.

# FIX (E501): split long dictionary lines so each fits within 79 chars.
parking_slots = {
    "P01": {"plate": "KA01AB1234", "hours": 2, "rate": 20.0,
            "is_occupied": True},
    "P02": {"plate": "TN07CD5678", "hours": 0, "rate": 20.0,
            "is_occupied": False},
    "P03": {"plate": "MH02EF9012", "hours": 4, "rate": 30.0,
            "is_occupied": True},
}

# FIX (W0603/C0103): replaced the reassigned global float
# 'total_collections' with a mutable dict, so no 'global' statement is needed.
parking_stats = {"total_collections": 0.0}


# FIX (C0103): renamed parkVehicle -> park_vehicle (snake_case).
# FIX (W0102): mutable default [] replaced with None.
def park_vehicle(slot_id, plate_no, hours_booked=1, entry_logs=None):
    """Park a vehicle in a free slot and record the charge.

    Returns True if the vehicle was parked, False otherwise.
    """
    # FIX (W0102): create a fresh list for every call.
    if entry_logs is None:
        entry_logs = []
    if slot_id not in parking_slots or parking_slots[slot_id]["is_occupied"]:
        return False
    parking_slots[slot_id]["plate"] = plate_no
    parking_slots[slot_id]["hours"] = hours_booked
    parking_slots[slot_id]["is_occupied"] = True
    parking_stats["total_collections"] += (
        parking_slots[slot_id]["rate"] * hours_booked
    )
    # FIX (C0209/E501): use an f-string split across lines.
    entry_logs.append(
        f"Vehicle {plate_no} parked at slot {slot_id} for "
        f"{hours_booked} hours with total charge calculated"
    )
    return True


# FIX (C0103): renamed releaseSlot -> release_slot.
def release_slot(slot_id):
    """Mark a slot as free. Returns False if the slot does not exist."""
    # FIX (W0702/E722/B110): catch only KeyError and report the failure
    # instead of a bare 'except: pass' that silently hides every error.
    try:
        parking_slots[slot_id]["is_occupied"] = False
        parking_slots[slot_id]["plate"] = ""
        parking_slots[slot_id]["hours"] = 0
    except KeyError:
        print(f"Slot {slot_id} does not exist")
        return False
    return True


# FIX (C0103): renamed checkSlotAvailability -> check_slot_availability.
def check_slot_availability(slot_id):
    """Return True if the slot exists and is not occupied."""
    # FIX (W0612/F841): removed unused variable 'overtime_fee'.
    # FIX (C0121/E711): use 'is None' instead of '== None'.
    if parking_slots.get(slot_id) is None:
        return False
    # FIX (R1703/R1705): return the boolean directly, no if/else needed.
    return not parking_slots[slot_id]["is_occupied"]


# FIX (C0103): renamed calculateParkingFee -> calculate_parking_fee.
# FIX (W0123/B307): removed eval(); the caller now passes a numeric
# surge multiplier instead of a code string to execute.
def calculate_parking_fee(slot_id, surge_multiplier=1.0):
    """Return the slot's base rate multiplied by the surge multiplier."""
    base_rate = parking_slots[slot_id]["rate"]
    # FIX (W0612/F841): base_rate is now actually used.
    return base_rate * float(surge_multiplier)


# FIX (C0103): renamed generateVehicleHash -> generate_vehicle_hash.
def generate_vehicle_hash(plate_no):
    """Return a SHA-256 hex digest of the plate number."""
    # FIX (B324): replaced weak MD5 with SHA-256.
    return hashlib.sha256(plate_no.encode()).hexdigest()


# FIX (C0103): renamed generateTicketPin -> generate_ticket_pin.
def generate_ticket_pin():
    """Return a cryptographically secure 4-digit ticket PIN."""
    # FIX (B311): secrets module instead of random.randint.
    return 1000 + secrets.randbelow(9000)


# FIX (C0103): renamed exportParkingManifest -> export_parking_manifest.
def export_parking_manifest(filename="parking_manifest.txt"):
    """Write the current slot state to a text file."""
    # FIX (R1732/W1514): use 'with' and an explicit encoding so the file
    # is always closed properly.
    with open(filename, "w", encoding="utf-8") as manifest:
        manifest.write(str(parking_slots))
    # FIX (B605): replaced os.system("echo ...") (shell injection risk)
    # with a plain print.
    print("Parking manifest exported to:", filename)


# FIX (C0103): renamed getAvailableSummary -> get_available_summary.
# FIX (W0621): parameter renamed so it no longer shadows the global.
def get_available_summary(slots):
    """Return the number of unoccupied slots."""
    # FIX (W0612): removed unused loop variable 's' by iterating values().
    return sum(1 for details in slots.values() if not details["is_occupied"])


def main():
    """Run a short demo of the parking lot system."""
    # FIX (hardcoded secret): read the key from an environment variable
    # instead of hardcoding it in the source.
    gate_barrier_key = os.environ.get("GATE_BARRIER_KEY")
    park_vehicle("P02", "DL03GH3456", 3)
    release_slot("P01")
    print("Is P02 available:", check_slot_availability("P02"))
    # FIX (B307): pass a number instead of the string "base_rate * 1.50".
    print("Surge Parking Fee:", calculate_parking_fee("P03", 1.50))
    print("Vehicle Hash:", generate_vehicle_hash("KA01AB1234"))
    print("Ticket PIN:", generate_ticket_pin())
    export_parking_manifest()
    print("Vacant slots:", get_available_summary(parking_slots))
    # FIX (sensitive data exposure): never print the secret key itself.
    print("Barrier Key active:", gate_barrier_key is not None)


# FIX: added main guard so importing the module does not run the demo.
# FIX (C0304/W292): file now ends with a newline.
if __name__ == "__main__":
    main()
