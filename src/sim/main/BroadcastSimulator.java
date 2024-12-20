package sim.main;

import sim.engine.*;
import static sim.utils.ConfigReader.*;
import sim.utils.*;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.stream.Collectors;
import java.util.stream.Stream;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.TimeUnit;

public class BroadcastSimulator {
	/**
	 *
	 */

	private BroadcastSimulator() {
	}

	static ExecutorService pool = Executors.newFixedThreadPool(8);

	public static Node[] generateNodes(int Nd, int Ts, int Tn, int Tb, double[] vs, double[] vn, double[] vb) {

		Node[] nodes = new Node[Nd];
		for (int i = 0; i < Nd; i++) {
			var n = new Node(Ts, Tn, Tb, vs, vn, vb);
			nodes[i] = n;
		}
		return nodes;

	}

	public static void run(String runID, Node[] nodes, int points, int tn, int ts, int tb) {
		int mb = 1024 * 1024;
		Runtime runtime = Runtime.getRuntime();
		long used_mem;

		for (int i = 0; i < nodes.length; i++) {
			var n = nodes[i];
			var l = new Logger("./results/r" + runID + "-d" + i + "-result.txt", points);

			for (int k = 0; k < points; k++) {
				n.run();

				l.log(n.getCurrentState());

			}
			used_mem = (runtime.totalMemory() - runtime.freeMemory()) / mb;
			System.out.println("Used Memory[MB]:" + used_mem);
			l.dump(false);
			System.gc();
		}

	}

	public static void main(String[] args) {

		int n_nodes = 2;
		final int points;

		if (args.length > 0) {
			points = Integer.parseInt(args[0]);
		} else {
			points = 5_000_000;
		}
		System.out.println("Points: " + points);
		try (Stream<Path> walk = Files.walk(Paths.get("."))) {

			var result = walk.filter(Files::isRegularFile).map(x -> x.toString())
					.filter((fn) -> fn.matches("(.*)config[0-9]+(.*)")).collect(Collectors.toList());
			System.out.println(result);
			result.forEach((fn) -> {

				var n = fn.replaceAll("\\D+", "");
				System.out.println("config" + n + ".txt");

				try {
					var config = readConfigFile("config" + n + ".txt");
					var nodes = generateNodes(n_nodes, config.Trx, config.Tn, config.Ttx, config.Vs, config.Vn,
							config.Vb);
					pool.execute(() -> run(n, nodes, points, config.Tn, config.Trx, config.Ttx));

				} catch (Exception e) {
					System.out.println(e.getMessage());
				}

			});

		} catch (IOException e) {
			System.out.println(e.getMessage());
		}
		pool.shutdown();
		try {
			pool.awaitTermination(10, TimeUnit.SECONDS);
		} catch (Exception e) {
			e.printStackTrace();
		}
	}

}