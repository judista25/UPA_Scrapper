plugins {
    kotlin("jvm") version "2.2.10"
    application
}

group = "com.marlin.tour.de.bier"
version = "1.0-SNAPSHOT"

repositories {
    mavenCentral()
}

dependencies {
    implementation(kotlin("stdlib"))  // Included by default, but explicit for clarity
    testImplementation(kotlin("test"))
}

tasks.test {
    useJUnitPlatform()
}
application {
    // Set this to the fully qualified name of your main class
    // If main.kt has no package, use "mainKt"
    mainClass.set("mainKt")
}
kotlin {
    jvmToolchain(17)
}

