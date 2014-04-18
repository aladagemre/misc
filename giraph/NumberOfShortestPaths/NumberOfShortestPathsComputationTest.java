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

import com.google.common.collect.Iterables;
import com.google.common.collect.Maps;
import org.apache.giraph.conf.GiraphConfiguration;
import org.apache.giraph.edge.ByteArrayEdges;
import org.apache.giraph.io.formats.IdWithValueTextOutputFormat;
import org.apache.giraph.io.formats.TextIntArrayNullTextInputFormat;
import org.apache.giraph.utils.InternalVertexRunner;
import org.apache.hadoop.io.Text;
import org.apache.log4j.Logger;
import org.junit.Test;

import java.security.SecurityPermission;
import java.util.Map;
import java.util.regex.Pattern;

import static org.apache.giraph.examples.NumberOfShortestPathsComputation.SOURCE_ID;
import static org.junit.Assert.*;

/**
 * Contains a simple unit test for {@link org.apache.giraph.examples.SimpleShortestPathsComputation}
 */
public class NumberOfShortestPathsComputationTest {
  /**
   * Seperator of tab
   */
  private static final Pattern SEPARATOR = Pattern.compile("[\t]");

  /** Class logger */
  private static final Logger LOG =
          Logger.getLogger(NumberOfShortestPathsComputationTest.class);

  /**
   * Test the behavior when a shorter path to a vertex has been found
   */
/*  @Test
  public void testOnShorterPathFound() throws Exception {
    Vertex<TextWritable, DoubleWritable, FloatWritable> vertex =
        new DefaultVertex<TextWritable, DoubleWritable, FloatWritable>();
    SimpleShortestPathsComputation computation =
        new SimpleShortestPathsComputation();
    MockUtils.MockedEnvironment<TextWritable, DoubleWritable, FloatWritable,
        DoubleWritable> env = MockUtils.prepareVertexAndComputation(vertex,
        new TextWritable(7L), new DoubleWritable(Double.MAX_VALUE), false,
        computation, 1L);
    Mockito.when(SOURCE_ID.get(env.getConfiguration())).thenReturn(2L);

    vertex.addEdge(EdgeFactory.create(
        new TextWritable(10L), new FloatWritable(2.5f)));
    vertex.addEdge(EdgeFactory.create(
        new TextWritable(20L), new FloatWritable(0.5f)));

    computation.compute(vertex, Lists.newArrayList(new DoubleWritable(2),
        new DoubleWritable(1.5)));

    assertTrue(vertex.isHalted());
    assertEquals(1.5d, vertex.getValue().get(), 0d);

    env.verifyMessageSent(new TextWritable(10L), new DoubleWritable(4));
    env.verifyMessageSent(new TextWritable(20L), new DoubleWritable(2));
  }
  */
  /**
   * Test the behavior when a new, but not shorter path to a vertex has been
   * found.
   */
  /*
  @Test
  public void testOnNoShorterPathFound() throws Exception {
    Vertex<TextWritable, DoubleWritable, FloatWritable> vertex =
        new DefaultVertex<TextWritable, DoubleWritable, FloatWritable>();
    SimpleShortestPathsComputation computation =
        new SimpleShortestPathsComputation();
    MockUtils.MockedEnvironment<TextWritable, DoubleWritable, FloatWritable,
        DoubleWritable> env = MockUtils.prepareVertexAndComputation(vertex,
        new TextWritable(7L), new DoubleWritable(0.5), false, computation, 1L);
    Mockito.when(SOURCE_ID.get(env.getConfiguration())).thenReturn(2L);

    vertex.addEdge(EdgeFactory.create(new TextWritable(10L),
        new FloatWritable(2.5f)));
    vertex.addEdge(EdgeFactory.create(
        new TextWritable(20L), new FloatWritable(0.5f)));

    computation.compute(vertex, Lists.newArrayList(new DoubleWritable(2),
        new DoubleWritable(1.5)));

    assertTrue(vertex.isHalted());
    assertEquals(0.5d, vertex.getValue().get(), 0d);

    env.verifyNoMessageSent();
  }
    */
  /**
   * A local integration test on toy data
   */
  @Test
  public void testToyData() throws Exception {
    String[] graph = new String[] {
        "A B C D E",
        "B A C F",
        "C A B F",
        "D A G H",
        "E A H",
        "F B C I",
        "G D I J",
        "H D E J",
        "I F G K",
        "J G H K",
        "K I J"
    };

    GiraphConfiguration conf = new GiraphConfiguration();
    // start from vertex A
    SOURCE_ID.set(conf, "A");
    conf.setComputationClass(NumberOfShortestPathsComputation.class);
    conf.setOutEdgesClass(ByteArrayEdges.class);
    conf.setVertexInputFormatClass(
        TextIntArrayNullTextInputFormat.class);
    conf.setVertexOutputFormatClass(
        IdWithValueTextOutputFormat.class);

    // run internally
    Iterable<String> results = InternalVertexRunner.run(conf, graph);

    Map<String, String> distances = parseDistances(results);


    // verify results
    assertNotNull(distances);
    assertEquals(11, distances.size());
    assertEquals("A\t[0, 0]", distances.get("A"));
    assertEquals("B\t[1, 1]", distances.get("B"));
    assertEquals("C\t[1, 1]", distances.get("C"));
    assertEquals("D\t[1, 1]", distances.get("D"));
    assertEquals("E\t[1, 1]", distances.get("E"));
    assertEquals("F\t[2, 2]", distances.get("F"));
    assertEquals("G\t[2, 1]", distances.get("G"));
    assertEquals("H\t[2, 2]", distances.get("H"));
    assertEquals("I\t[3, 3]", distances.get("I"));
    assertEquals("J\t[3, 3]", distances.get("J"));
    assertEquals("K\t[4, 6]", distances.get("K"));
  }

  private Map<String, String> parseDistances(Iterable<String> results) {
    String id;
    Integer value, distance, ways;
    String str;
    Map<String, String> distances =
        Maps.newHashMapWithExpectedSize(Iterables.size(results));
    for (String line : results) {
      LOG.info(line);
      id = line.trim().substring(0, 1);
      distances.put(id, line);
    }
    return distances;
  }
}
