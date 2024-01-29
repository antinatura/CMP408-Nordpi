#include <linux/init.h>
#include <linux/module.h>
#include <linux/gpio.h>
#include <linux/interrupt.h>
#include <linux/fs.h>
#include <linux/uaccess.h>

MODULE_LICENSE("GPL");
MODULE_AUTHOR("Ance Strazdina");
MODULE_DESCRIPTION("Button Interrupt Userpsace Notify Module");

#define BUTTON_GPIO_PIN 16 // button pin, code assumes the button is placed correctly
#define GPIO_DESC "Button Interrupt"

static int major_number;
static struct class *button_class;
static struct device *button_device;
static int button_pressed;
static char message = 'B';  // button press signal message

// button interrupt handler
static irqreturn_t button_irq(int irq, void *dev_id) {
    pr_info("Button pressed!\n");
    button_pressed = 1;  // button is pressed flag

    // notify user space by writing to the char device
    if (button_device) {
        size_t ret = copy_to_user(button_device, &message, sizeof(char)); // write button press signal message to char device (immediate userspace notify)

        // return will be empty if successful, but if return is not empty catch it
        if (ret != 0) {
            pr_err("Failed to copy data to userspace\n");
            return -EFAULT;
        }
    }

    return IRQ_HANDLED;
}

// calback for button char device being opened by the userspace app
static int button_open(struct inode *inode, struct file *file) {
    pr_info("Button char device opened\n");
    return 0;
}

// callback for button char device being read by the userspace app
static ssize_t button_read(struct file *file, char *buffer, size_t len, loff_t *offset) {
    if (button_pressed) {
        button_pressed = 0;  // reset the button press flag
        return copy_to_user(buffer, &message, sizeof(char)) ? -EFAULT : 1; // write button press signal message to char device (userspace notify if char dev file is read after button press)
    } else {
        return 0;  // button has not been pressed, no data available
    }
}

// calback for button charr device being closed by the userspace app
static int button_release(struct inode *inode, struct file *file) {
    pr_info("Button char device closed\n");
    return 0;
}

// functions to handle the userspace app opening, reading, and closing the button char device
static struct file_operations fops = {
    .open = button_open,
    .read = button_read,
    .release = button_release,
};

// initialise function
static int __init button_init(void) {
    // request gpio
    if (gpio_request(BUTTON_GPIO_PIN, GPIO_DESC) < 0) {
        pr_err("Failed to request GPIO %d\n", BUTTON_GPIO_PIN);
        return -ENODEV;
    }

    // configure gpio
    if (gpio_direction_input(BUTTON_GPIO_PIN) < 0) {
        pr_err("Failed to set GPIO %d as input\n", BUTTON_GPIO_PIN);
        gpio_free(BUTTON_GPIO_PIN);
        return -ENODEV;
    }

    // request irq for the gpio pin
    if (request_irq(gpio_to_irq(BUTTON_GPIO_PIN), button_irq, IRQF_TRIGGER_RISING, GPIO_DESC, NULL) < 0) {
        pr_err("Failed to request IRQ for GPIO %d\n", BUTTON_GPIO_PIN);
        gpio_free(BUTTON_GPIO_PIN);
        return -ENODEV;
    }

    major_number = register_chrdev(0, "button_char", &fops); // register button character device
    
    // create button class and character device: /dev/button_dev
    button_class = class_create(THIS_MODULE, "button_class");
    button_device = device_create(button_class, NULL, MKDEV(major_number, 0), NULL, "button_dev");

    pr_info("Button interrupt module loaded\n");
    return 0;
}

static void __exit button_exit(void) {
    // destroy device and class
    device_destroy(button_class, MKDEV(major_number, 0));
    class_unregister(button_class);
    class_destroy(button_class);

    unregister_chrdev(major_number, "button_char"); // unregister character device

    // free irq and gpio
    free_irq(gpio_to_irq(BUTTON_GPIO_PIN), NULL);
    gpio_free(BUTTON_GPIO_PIN);

    pr_info("Button interrupt module unloaded\n");
}

module_init(button_init);
module_exit(button_exit);