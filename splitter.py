import reedsolo
import random
import sys
from typing import List


def divide_into_packets(data: List[int], packet_size: int) -> List[List[int]]:
    """
    Divide data into packets of specified size.
    """
    return [data[i:i+packet_size] for i in range(0, len(data), packet_size)]

def add_redundancy(packet: List[int], redundancy_symbols: int) -> bytes:
    """
    Add redundancy to a packet using Reed-Solomon encoding.
    """
    rs = reedsolo.RSCodec(redundancy_symbols)
    return rs.encode(packet)

def is_encoding_cycle_success(packet_size: int = 10, data_size: int = 100, loss_percentage: int = 90) -> bool:
    """_summary_

    Args:
        packet_size (int, optional): The size of the packets to send, in bytes. Defaults to 10.
        data_size (int, optional): The amount of data in total, in bytes. Defaults to 100.
        loss_percentage (int, optional): The percentage of packets to delete in the test.

    Returns:
        bool: True if the encoded -> random delete -> decode cycle recovered original data. False otherwise.
    """
    # Original data (numbers 0 through 99)
    original_data: List[int] = random.randbytes(data_size)

    # Divide data into packets
    packets: List[List[int]] = divide_into_packets(original_data, packet_size)

    # Add redundancy to each packet
    redundancy_symbols: int = len(packets) - packet_size
    redundant_packets: List[bytes] = [add_redundancy(packet, redundancy_symbols) for packet in packets]

    # Simulate packet loss by removing some packets (let's say, 90%)
    num_packets_to_remove: int = len(packets) // loss_percentage
    indices_to_remove: List[int] = random.sample(range(len(packets)), num_packets_to_remove)
    transmitted_packets: List[bytes] = [packet for i, packet in enumerate(redundant_packets) if i not in indices_to_remove]

    # Decode the transmitted packets to recover original data
    rs = reedsolo.RSCodec(redundancy_symbols)
    decoded_data: List[int] = []
    for packet in transmitted_packets:
        try:
            decoded_packet: List[int] = rs.decode(packet)
            # Dont stitch back packets that are empty.
            if decoded_packet != bytearray():
                decoded_data.extend(decoded_packet[:packet_size])  # Extract only original symbols
        except reedsolo.ReedSolomonError:
            pass  # Unable to recover this packet due to excessive loss
        
    decoded_data = b"".join(decoded_data)

    if original_data == decoded_data:
        return True
    else:
        return False

def main():
    try:
        iterations = sys.argv[1]
    except IndexError:
        iterations = 1000

    successes = 0
    for _ in range(iterations):
        if is_encoding_cycle_success():
            successes += 1
            
    print(f"Successes {successes}")
    print(f"Failures  {iterations - successes}")
        

if __name__ == "__main__":
    main()