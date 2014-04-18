/*
 * Licensed to the Apache Software Foundation (ASF) under one
 * or more contributor license agreements.  See the NOTICE file
 * distributed with this work for additional information
 * regarding copyright ownership.  The ASF licenses this file
 * to you under the Apache License, Version 2.0 (the
 * "License"); you may not use this file except in compliance
 * with the License.  You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

package org.apache.giraph.examples;

import org.apache.giraph.conf.StrConfOption;
import org.apache.giraph.graph.BasicComputation;
import org.apache.giraph.graph.Vertex;
import org.apache.giraph.utils.IntArrayListWritable;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.NullWritable;
import org.apache.hadoop.io.Text;
import org.apache.log4j.Logger;

import java.io.IOException;

/**
 * Demonstrates the basic Pregel shortest paths implementation.
 */
@Algorithm(
    name = "Shortest paths",
    description = "Finds all shortest paths from a selected vertex"
)
public class NumberOfShortestPathsComputation extends BasicComputation<
    Text, IntArrayListWritable, NullWritable, IntArrayListWritable> {
  /** The shortest paths id */
  public static final StrConfOption SOURCE_ID =
      new StrConfOption("NumberOfShortestPathsVertex.sourceId", "A",
          "The shortest paths id");
  /** Class logger */
  private static final Logger LOG =
      Logger.getLogger(NumberOfShortestPathsComputation.class);

  /**
   * Is this vertex the source id?
   *
   * @param vertex Vertex
   * @return True if the source id
   */
  private boolean isSource(Vertex<Text, ?, ?> vertex) {
    return vertex.getId().toString().equals(SOURCE_ID.get(getConf()));
  }

  /**
   * Returns the distance of current vertex.
   * @param vertex current vertex object
   * @return distance of current vertex to the source.
   */
  private int getDistance(Vertex<Text, IntArrayListWritable,
    NullWritable> vertex) {
    return vertex.getValue().get(0).get();
  }

  /**
   * Returns the number of possible ways from source to this vertex.
   * @param vertex current vertex object
   * @return number of shortest ways from the source to this vertex.
   */
  private int getWays(Vertex<Text, IntArrayListWritable, NullWritable> vertex) {
    return vertex.getValue().get(1).get();
  }

  @Override
  public void compute(
      Vertex<Text, IntArrayListWritable, NullWritable> vertex,
      Iterable<IntArrayListWritable> messages) throws IOException {
    if (getSuperstep() == 0) {
      int value = isSource(vertex) ? 0 : Integer.MAX_VALUE - 1;
      IntArrayListWritable pair = new IntArrayListWritable();
      IntWritable valueWritable = new IntWritable(value);
      pair.add(valueWritable);
      pair.add(valueWritable);
      vertex.setValue(pair);
    }
    int sumWayMessages = 0;
    int distance;
    int oldDistance = getDistance(vertex);
    int minDistance = oldDistance;
    int minWay = getWays(vertex);
    int way;
    boolean changed = false;

    for (IntArrayListWritable message : messages) {
      distance = message.get(0).get();
      minDistance = Math.min(distance, minDistance);

      if (distance < oldDistance) {
        way = message.get(1).get();
        sumWayMessages += way;
      }
    }

    if (minDistance < getDistance(vertex)) {
      changed = true;
    }



    LOG.info("Vertex " + vertex.getId() + " got sumMessages = " +
            sumWayMessages + " vertex value = " + vertex.getValue());

    if (changed && sumWayMessages < getWays(vertex)) {
      minWay = sumWayMessages;
    }
    if (changed) {
      IntArrayListWritable newValue = new IntArrayListWritable();
      newValue.add(new IntWritable(minDistance));
      newValue.add(new IntWritable(minWay));
      vertex.setValue(newValue);

    }

    if (minDistance < oldDistance || oldDistance == 0) {
      IntArrayListWritable outMessage = new IntArrayListWritable();
      outMessage.add(new IntWritable(minDistance + 1));
      outMessage.add(new IntWritable(minWay > 0 ? minWay : 1));
      LOG.info("Vertex " + vertex.getId() + " is sending " + outMessage);
      sendMessageToAllEdges(vertex, outMessage);
    }


    vertex.voteToHalt();
  }



}
