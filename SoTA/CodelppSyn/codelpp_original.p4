/*
* Copyright 2018-present Ralf Kundel, Nikolas Eller
*
* Licensed under the Apache License, Version 2.0 (the "License");
* you may not use this file except in compliance with the License.
* You may obtain a copy of the License at
*
*    http://www.apache.org/licenses/LICENSE-2.0
*
* Unless required by applicable law or agreed to in writing, software
* distributed under the License is distributed on an "AS IS" BASIS,
* WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
* See the License for the specific language governing permissions and
* limitations under the License.
*/

#include <core.p4>
#include <v1model.p4>

//Codel
#define SOJOURN_TARGET 500 //in usec - 0.35ms
#define CONTROL_INTERVAL 48w10000//in usec - 10 ms - RTT
#define INTERFACE_MTU 1500
#define NO_QUEUE_ID 32w64

register<bit<32>>(NO_QUEUE_ID) r_drop_count;
register<bit<48>>(NO_QUEUE_ID) r_drop_time;
register<bit<32>>(NO_QUEUE_ID) r_last_drop_count;
register<bit<48>>(NO_QUEUE_ID) r_next_drop;
register<bit<1>>(NO_QUEUE_ID) r_state_dropping;

//Prio Drop
register<bit<1>>(NO_QUEUE_ID) r_slice_drop_0;
register<bit<1>>(NO_QUEUE_ID) r_slice_drop_1;
register<bit<1>>(NO_QUEUE_ID) r_slice_drop_2;
register<bit<1>>(NO_QUEUE_ID) r_slice_drop_3;
register<bit<1>>(NO_QUEUE_ID) r_slice_drop_4;
register<bit<1>>(NO_QUEUE_ID) r_slice_drop_5; 
register<bit<1>>(NO_QUEUE_ID) r_slice_drop_6;
register<bit<1>>(NO_QUEUE_ID) r_slice_drop_7;

//Timestamp
register<bit<32>>(NO_QUEUE_ID) r_slice_time_0;
register<bit<32>>(NO_QUEUE_ID) r_slice_time_1;
register<bit<32>>(NO_QUEUE_ID) r_slice_time_2;
register<bit<32>>(NO_QUEUE_ID) r_slice_time_3;
register<bit<32>>(NO_QUEUE_ID) r_slice_time_4;
register<bit<32>>(NO_QUEUE_ID) r_slice_time_5;
register<bit<32>>(NO_QUEUE_ID) r_slice_time_6;
register<bit<32>>(NO_QUEUE_ID) r_slice_time_7;

//enq_qdepth
register<bit<19>>(NO_QUEUE_ID) r_slice_enq_0;
register<bit<19>>(NO_QUEUE_ID) r_slice_enq_1;
register<bit<19>>(NO_QUEUE_ID) r_slice_enq_2;
register<bit<19>>(NO_QUEUE_ID) r_slice_enq_3;
register<bit<19>>(NO_QUEUE_ID) r_slice_enq_4;
register<bit<19>>(NO_QUEUE_ID) r_slice_enq_5;
register<bit<19>>(NO_QUEUE_ID) r_slice_enq_6;
register<bit<19>>(NO_QUEUE_ID) r_slice_enq_7;

//deq_qdepth
register<bit<19>>(NO_QUEUE_ID) r_slice_deq_0;
register<bit<19>>(NO_QUEUE_ID) r_slice_deq_1;
register<bit<19>>(NO_QUEUE_ID) r_slice_deq_2;
register<bit<19>>(NO_QUEUE_ID) r_slice_deq_3;
register<bit<19>>(NO_QUEUE_ID) r_slice_deq_4;
register<bit<19>>(NO_QUEUE_ID) r_slice_deq_5;
register<bit<19>>(NO_QUEUE_ID) r_slice_deq_6;
register<bit<19>>(NO_QUEUE_ID) r_slice_deq_7;


//Header


struct codel_t {
    bit<48> drop_time;
    bit<48> time_now;
    bit<1>  ok_to_drop;
    bit<1>  state_dropping;
    bit<32> delta;
    bit<48> time_since_last_dropping;
    bit<48> drop_next;
    bit<32> drop_cnt;
    bit<32> last_drop_cnt;
    bit<1>  reset_drop_time;
    bit<48> new_drop_time;
    bit<48> new_drop_time_helper;
    bit<9>  queue_id;
}

struct prio_t {
	bit<1>  prio_drop;
	bit<32> time;
	bit<19> enq;
	bit<19> deq;
}

header ethernet_t {
    bit<48> dst_addr;
    bit<48> src_addr;
    bit<16> ethertype;
}

header ipv4_t {
    bit<4>  version;
    bit<4>  ihl;
    bit<8>  diffserv;
    bit<16> totalLen;
    bit<16> identification;
    bit<3>  flags;
    bit<13> fragOffset;
    bit<8>  ttl;
    bit<8>  protocol;
    bit<16> hdrChecksum;
    bit<32> srcAddr;
    bit<32> dstAddr;
}

header udp_t {
    bit<16> sourcePort;
    bit<16> destPort;
    bit<16> length_;
    bit<16> checksum;
}

header tcp_t {
    bit<16> srcPort;
    bit<16> dstPort;
    bit<32> seqNo;
    bit<32> ackNo;
    bit<4>  dataOffset;
    bit<4>  res;
    bit<8>  flags;
    bit<16> window;
    bit<16> checksum;
    bit<16> urgentPtr;
}



struct headers {
    ethernet_t    ethernet; 
    ipv4_t        ipv4; 
    tcp_t         tcp;
    udp_t         udp;
}

struct metadata {
    codel_t      codel; 
    prio_t		 prio;
}



//Parser
parser ParserImpl(packet_in packet, out headers hdr, inout metadata meta, inout standard_metadata_t standard_metadata) {
    state start {
        packet.extract(hdr.ethernet);
        transition select(hdr.ethernet.ethertype) {
            16w0x800: parse_ipv4;
            default: accept;
        }
    }

    state parse_ipv4 {
        packet.extract(hdr.ipv4);
        transition select(hdr.ipv4.protocol) {
            8w17: parse_udp;
            8w6: parse_tcp;
            default: accept;
        }
    }
    
    state parse_tcp {
        packet.extract(hdr.tcp);
	transition accept;

    }
    
    state parse_udp {
        packet.extract(hdr.udp);
	transition accept;
    }


}

//Ingress
control ingress(inout headers hdr, inout metadata meta, inout standard_metadata_t standard_metadata) {
    action drop() {
        mark_to_drop(standard_metadata);
    }
    	
    action forward_slicing(bit<9> egress_spec, bit<48> dst_mac) {
        standard_metadata.egress_spec = egress_spec;
        standard_metadata.egress_port = egress_spec;
        hdr.ethernet.dst_addr = dst_mac;
        hdr.ipv4.ttl = hdr.ipv4.ttl -1;
    }
    table slice_forwarding {
    	key = {
            hdr.ipv4.srcAddr              : exact;
            hdr.ipv4.dstAddr              : exact;
            
        }
        
        actions = {
            forward_slicing;
            drop;
            NoAction;
        }
        size = 1024;
        default_action = NoAction();
    }
        
    action set_priority(bit<7> value) {
        standard_metadata.priority = (bit<3>)value;
    }
    
    table slice_priority{
    	key = {
            hdr.ipv4.srcAddr: exact;            
        }
        actions = {
            set_priority;
        }
        default_action = set_priority((bit<7>) 0);
        size = 32;
    }
    
    apply {
       slice_forwarding.apply();
       slice_priority.apply();
       
       
       if (standard_metadata.priority == 3w7){
       	r_slice_drop_7.read(meta.prio.prio_drop, (bit<32>)standard_metadata.egress_port);
       	
       }else if (standard_metadata.priority == 3w6){
               r_slice_drop_6.read(meta.prio.prio_drop, (bit<32>)standard_metadata.egress_port);
       
       }else if (standard_metadata.priority == 3w5){
       	r_slice_drop_5.read(meta.prio.prio_drop, (bit<32>)standard_metadata.egress_port);
       
       }else if (standard_metadata.priority == 3w4){
       	r_slice_drop_4.read(meta.prio.prio_drop, (bit<32>)standard_metadata.egress_port);
       
       }else if (standard_metadata.priority == 3w3){
       	r_slice_drop_3.read(meta.prio.prio_drop, (bit<32>)standard_metadata.egress_port);
       
       }else if (standard_metadata.priority == 3w2){
       	r_slice_drop_2.read(meta.prio.prio_drop, (bit<32>)standard_metadata.egress_port);
       
       }else if (standard_metadata.priority == 3w1){
       	r_slice_drop_1.read(meta.prio.prio_drop, (bit<32>)standard_metadata.egress_port);
       
       }else if (standard_metadata.priority == 3w0){
       	r_slice_drop_0.read(meta.prio.prio_drop, (bit<32>)standard_metadata.egress_port);
       
       }
       
       if (meta.prio.prio_drop==1w1){
		mark_to_drop(standard_metadata);
	}
       
    }
}

//Checksum
control verifyChecksum(inout headers hdr, inout metadata meta) {
    apply {
    }
}

control c_codel(inout headers hdr, inout metadata meta, inout standard_metadata_t standard_metadata) {

    action a_codel_control_law(bit<48> value) {
        meta.codel.drop_next = meta.codel.time_now + value;
        r_next_drop.write((bit<32>)meta.codel.queue_id, (bit<48>)meta.codel.drop_next);
    }

    action a_codel_init() {
        meta.codel.ok_to_drop = 1w0;
        meta.codel.time_now = (bit<48>)standard_metadata.enq_timestamp + (bit<48>)standard_metadata.deq_timedelta;
        meta.codel.new_drop_time = meta.codel.time_now + CONTROL_INTERVAL;
        r_state_dropping.read(meta.codel.state_dropping, (bit<32>)meta.codel.queue_id);
        r_drop_count.read(meta.codel.drop_cnt, (bit<32>)meta.codel.queue_id);
        r_last_drop_count.read(meta.codel.last_drop_cnt, (bit<32>)meta.codel.queue_id);
        r_next_drop.read(meta.codel.drop_next, (bit<32>)meta.codel.queue_id);
        r_drop_time.read(meta.codel.drop_time, (bit<32>)meta.codel.queue_id);
    }

    action a_go_to_drop_state() {
	    mark_to_drop(standard_metadata);
        r_state_dropping.write((bit<32>)meta.codel.queue_id, (bit<1>)1);
        meta.codel.delta = meta.codel.drop_cnt - meta.codel.last_drop_cnt;
        meta.codel.time_since_last_dropping = meta.codel.time_now - meta.codel.drop_next;
        meta.codel.drop_cnt = 32w1;
        r_drop_count.write((bit<32>)meta.codel.queue_id, (bit<32>)1);
    }

    table t_codel_control_law {
        actions = {
            a_codel_control_law;
        }
        key = {
            meta.codel.drop_cnt: lpm;
        }
        size = 32;
    }

    apply {
        a_codel_init();
    
        if (standard_metadata.deq_timedelta < SOJOURN_TARGET ) { //|| standard_metadata.deq_qdepth < 19w1
            meta.codel.reset_drop_time = 1w1;
        }
            
        if (meta.codel.reset_drop_time == 1w1) {
            r_drop_time.write((bit<32>)meta.codel.queue_id, (bit<48>)0);
            meta.codel.drop_time = 48w0; // if queueing time < SOJOURN_TARGET, reset the drop_time to 0
        }
        else { // not reset the drop_time
            if (meta.codel.drop_time == 48w0) {
                r_drop_time.write((bit<32>)meta.codel.queue_id, (bit<48>)meta.codel.new_drop_time);
                meta.codel.drop_time = meta.codel.new_drop_time;
            }
            else { //if (meta.codel.drop_time > 48w0)
                if (meta.codel.time_now >= meta.codel.drop_time) {
                    meta.codel.ok_to_drop = 1w1;

                }
            }
        }

        if (meta.codel.state_dropping == 1w1) {
            if (meta.codel.ok_to_drop == 1w0) {
                r_state_dropping.write((bit<32>)meta.codel.queue_id, (bit<1>)0); //leave drop state
            }
            else { // if_4
                if (meta.codel.time_now >= meta.codel.drop_next) {
                    if(standard_metadata.priority == 3w0){
                        mark_to_drop(standard_metadata);
				        meta.codel.drop_cnt = meta.codel.drop_cnt + 32w1;
        	            r_drop_count.write((bit<32>)meta.codel.queue_id, (bit<32>)meta.codel.drop_cnt);
                        t_codel_control_law.apply();
                    }
                }
            }
        }
        else { // not in the dropping state
            if (meta.codel.ok_to_drop == 1w1) {
                if(standard_metadata.priority == 3w0){
                    a_go_to_drop_state();
                }
                if (meta.codel.delta > 32w1 && meta.codel.time_since_last_dropping < CONTROL_INTERVAL*16) { // if_3, only when priority is 0
                    r_drop_count.write((bit<32>)meta.codel.queue_id, (bit<32>)meta.codel.delta);
                    meta.codel.drop_cnt = meta.codel.delta;
                }
                r_last_drop_count.write((bit<32>)meta.codel.queue_id, (bit<32>)meta.codel.drop_cnt);
                t_codel_control_law.apply();
            }
        }
    }
}

//Egress
control egress(inout headers hdr, inout metadata meta, inout standard_metadata_t standard_metadata) {

	c_codel() c_codel_0;
    
    apply {
        meta.codel.queue_id = standard_metadata.egress_port;
        
        
        if (standard_metadata.priority == 3w7){
        	r_slice_time_7.write((bit<32>)meta.codel.queue_id, (bit<32>)standard_metadata.deq_timedelta);
		r_slice_enq_7.write((bit<32>)meta.codel.queue_id, (bit<19>)standard_metadata.enq_qdepth);
		r_slice_deq_7.write((bit<32>)meta.codel.queue_id, (bit<19>)standard_metadata.deq_qdepth);
	
       	if (standard_metadata.deq_qdepth > 19w700){
	   		r_slice_drop_7.write((bit<32>)meta.codel.queue_id, (bit<1>)1);
		}else{
	   		r_slice_drop_7.write((bit<32>)meta.codel.queue_id, (bit<1>)0);	
		}
       	
       }else if (standard_metadata.priority == 3w6){
       	r_slice_time_6.write((bit<32>)meta.codel.queue_id, (bit<32>)standard_metadata.deq_timedelta);
		r_slice_enq_6.write((bit<32>)meta.codel.queue_id, (bit<19>)standard_metadata.enq_qdepth);
		r_slice_deq_6.write((bit<32>)meta.codel.queue_id, (bit<19>)standard_metadata.deq_qdepth);
       
       	if (standard_metadata.deq_qdepth > 19w450){
	   		r_slice_drop_6.write((bit<32>)meta.codel.queue_id, (bit<1>)1);
		}else{
	   		r_slice_drop_6.write((bit<32>)meta.codel.queue_id, (bit<1>)0);	
		}
       
       }else if (standard_metadata.priority == 3w5){
       	r_slice_time_5.write((bit<32>)meta.codel.queue_id, (bit<32>)standard_metadata.deq_timedelta);
		r_slice_enq_5.write((bit<32>)meta.codel.queue_id, (bit<19>)standard_metadata.enq_qdepth);
		r_slice_deq_5.write((bit<32>)meta.codel.queue_id, (bit<19>)standard_metadata.deq_qdepth);
       	
       	if (standard_metadata.deq_qdepth > 19w400){
	   		r_slice_drop_5.write((bit<32>)meta.codel.queue_id, (bit<1>)1);
		}else{
	   		r_slice_drop_5.write((bit<32>)meta.codel.queue_id, (bit<1>)0);	
		}
       
       }else if (standard_metadata.priority == 3w4){
       	if (standard_metadata.deq_qdepth > 19w300){
	   		r_slice_drop_4.write((bit<32>)meta.codel.queue_id, (bit<1>)1);
		}else{
	   		r_slice_drop_4.write((bit<32>)meta.codel.queue_id, (bit<1>)0);	
		}
       
       }else if (standard_metadata.priority == 3w3){
       	r_slice_time_3.write((bit<32>)meta.codel.queue_id, (bit<32>)standard_metadata.deq_timedelta);
		r_slice_enq_3.write((bit<32>)meta.codel.queue_id, (bit<19>)standard_metadata.enq_qdepth);
		r_slice_deq_3.write((bit<32>)meta.codel.queue_id, (bit<19>)standard_metadata.deq_qdepth);
       	
       	if (standard_metadata.deq_qdepth > 19w200){
	   		r_slice_drop_3.write((bit<32>)meta.codel.queue_id, (bit<1>)1);
		}else{
	   		r_slice_drop_3.write((bit<32>)meta.codel.queue_id, (bit<1>)0);	
		}
       
       }else if (standard_metadata.priority == 3w2){
       	r_slice_time_2.write((bit<32>)meta.codel.queue_id, (bit<32>)standard_metadata.deq_timedelta);
		r_slice_enq_2.write((bit<32>)meta.codel.queue_id, (bit<19>)standard_metadata.enq_qdepth);
		r_slice_deq_2.write((bit<32>)meta.codel.queue_id, (bit<19>)standard_metadata.deq_qdepth);
       	
       	if (standard_metadata.deq_qdepth > 19w100){
	   		r_slice_drop_2.write((bit<32>)meta.codel.queue_id, (bit<1>)1);
		}else{
	   		r_slice_drop_2.write((bit<32>)meta.codel.queue_id, (bit<1>)0);	
		}
       
       }else if (standard_metadata.priority == 3w1){
       	r_slice_time_1.write((bit<32>)meta.codel.queue_id, (bit<32>)standard_metadata.deq_timedelta);
		r_slice_enq_1.write((bit<32>)meta.codel.queue_id, (bit<19>)standard_metadata.enq_qdepth);
		r_slice_deq_1.write((bit<32>)meta.codel.queue_id, (bit<19>)standard_metadata.deq_qdepth);
       
       	if (standard_metadata.deq_qdepth > 19w40){
	   		r_slice_drop_1.write((bit<32>)meta.codel.queue_id, (bit<1>)1);
		}else{
	   		r_slice_drop_1.write((bit<32>)meta.codel.queue_id, (bit<1>)0);	
		}
       
       }else if (standard_metadata.priority == 3w0){
        	r_slice_time_0.write((bit<32>)meta.codel.queue_id, (bit<32>)standard_metadata.deq_timedelta);
		r_slice_enq_0.write((bit<32>)meta.codel.queue_id, (bit<19>)standard_metadata.enq_qdepth);
		r_slice_deq_0.write((bit<32>)meta.codel.queue_id, (bit<19>)standard_metadata.deq_qdepth);
		
       	if (standard_metadata.deq_qdepth > 19w10){
	   		r_slice_drop_0.write((bit<32>)meta.codel.queue_id, (bit<1>)1);
		}else{
	   		r_slice_drop_0.write((bit<32>)meta.codel.queue_id, (bit<1>)0);	
	    }
       
       }
        c_codel_0.apply(hdr, meta, standard_metadata);
	}
}


control computeChecksum(inout headers hdr, inout metadata meta) {
    apply {
        update_checksum(
           true, 
          { hdr.ipv4.version, 
            hdr.ipv4.ihl, 
            hdr.ipv4.diffserv, 
            hdr.ipv4.totalLen, 
            hdr.ipv4.identification, 
            hdr.ipv4.flags, 
            hdr.ipv4.fragOffset, 
            hdr.ipv4.ttl, 
            hdr.ipv4.protocol, 
            hdr.ipv4.srcAddr, 
            hdr.ipv4.dstAddr 
          }, 
            hdr.ipv4.hdrChecksum, 
            HashAlgorithm.csum16);

    }
}


//Deparser
control DeparserImpl(packet_out packet, in headers hdr) {
    apply {
        packet.emit(hdr.ethernet);
        packet.emit(hdr.ipv4);
        packet.emit(hdr.tcp);
        packet.emit(hdr.udp);
    }
}

//Init Switch
V1Switch(ParserImpl(), verifyChecksum(), ingress(), egress(), computeChecksum(), DeparserImpl()) main;

//end
