package fachstudie.iot;

import com.google.api.client.json.jackson2.*;
import com.google.api.client.util.*;
import com.google.cloud.dataflow.sdk.*;
import com.google.cloud.dataflow.sdk.io.*;
import com.google.cloud.dataflow.sdk.options.*;
import com.google.cloud.dataflow.sdk.transforms.*;

public class IoTPipeline {
	public static class Brightness {
		@Key private double brightness;
	}

	public static class HueCommand {
		@Key private boolean on = true;
		@Key private double hue, sat, bri;
	}

	public static void main(String[] args) {
		final String readTopic = "<Pub/Sub topic to read from>";
		final String writeTopic = "<Pub/Sub topic to write to>";

		// Set dataflow options
		PipelineOptions options = PipelineOptionsFactory.fromArgs(args).withValidation().create();
		DataflowPipelineOptions dataflowOptions = options.as(DataflowPipelineOptions.class);

		dataflowOptions.setStreaming(true);
		dataflowOptions.setZone("europe-west1-b");
		dataflowOptions.setDiskSizeGb(2);
		dataflowOptions.setWorkerMachineType("n1-standard-1");

		// Create and set up the pipeline
		Pipeline pipeline = Pipeline.create(options);

		pipeline
		// Read from Pub/Sub topic
		.apply(PubsubIO.Read.topic(readTopic))
		// Create command for Hue Lamp
		.apply(ParDo.of(new DoFn<String, String>() {
			private static final long serialVersionUID = 1L;
			@Override
			public void processElement(DoFn<String, String>.ProcessContext c) throws Exception {
				JacksonFactory jsonFactory = new JacksonFactory();

				String input = new String(Base64.decodeBase64(c.element()));
				Brightness value = jsonFactory.fromString(input, Brightness.class);

				HueCommand command = new HueCommand();
				command.hue = 6000;
				command.sat = Math.min(255, (int) (value.brightness * 400));
				command.bri = Math.max(0, Math.min(255, (int) (555 - value.brightness * 600)));

				String json = jsonFactory.toString(command);
				c.output(Base64.encodeBase64String(json.getBytes()));
			}
		}))
		// Write to Pub/Sub topic
		.apply(PubsubIO.Write.topic(writeTopic));

		// Start the pipeline
		pipeline.run();
	}
}
