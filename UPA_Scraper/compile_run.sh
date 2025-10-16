# Make gradlew executable (in case permissions change)
chmod +x gradlew

# Clean and build the distribution TAR (or use 'build' for just compiling)
./gradlew clean distTar

# Extract the TAR (adjust version if changed in build.gradle.kts)
tar -xvf build/distributions/my-kotlin-app-1.0-SNAPSHOT.tar -C build/distributions/

# Run the app (pass args if needed, e.g., "$@" to forward script args)
build/distributions/UPA_Scraper-1.0-SNAPSHOT/bin/my-kotlin-app

